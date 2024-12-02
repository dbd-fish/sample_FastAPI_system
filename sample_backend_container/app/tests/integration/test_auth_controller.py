import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.core.security import verify_password
from app.config.test_data import TestData
from main import app
from app.database import configure_database, Base
from app.schemas.user import UserCreate
from app.core.log_config import configure_logging
from app.seeders.seed_data import clear_data, seed_data
from app.services.auth_service import get_current_user
from app.models.user import User
from passlib.context import CryptContext
from app.database import engine, AsyncSessionLocal, Base
from typing import AsyncGenerator

@pytest.mark.asyncio(loop_scope='session')
async def test_register_user(regist_user_data: UserCreate, db_session: AsyncSession) -> None:
    """
    ユーザー登録のテスト。
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost:8000") as client:
        response = await client.post("/auth/register", json=regist_user_data.model_dump())
        assert response.status_code == 200
        assert response.json()["msg"] == "User created successfully"

        # データベース内のユーザーを確認
        result = await db_session.execute(
            select(User).where(User.email == regist_user_data.email)
        )
        user: Optional[User] = result.scalars().first()
        assert user is not None
        assert user.email == regist_user_data.email
        assert user.username == regist_user_data.username

@pytest.mark.asyncio(loop_scope='session')
async def test_register_existing_user(regist_user_data: UserCreate, db_session: AsyncSession) -> None:
    """
    既に存在するメールアドレスでユーザー登録を試みた場合のテスト。
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost:8000") as client:
        # 最初の登録は成功する
        response = await client.post("/auth/register", json=regist_user_data.model_dump())
        assert response.status_code == 200

        # 同じメールアドレスで再登録を試みる
        response = await client.post("/auth/register", json=regist_user_data.model_dump())
        assert response.status_code == 400
        assert "User already exists" in response.json()["detail"]

@pytest.mark.asyncio(loop_scope='session')
async def test_login_user() -> None:
    """
    ログイン処理のテスト。
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost:8000/") as client:
        response = await client.post(
            "/auth/login",
            data={"username": TestData.TEST_USER_EMAIL_1, "password": TestData.TEST_USER_PASSWORD},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        assert response.status_code == 200
        assert "access_token" in response.json()

@pytest.mark.asyncio(loop_scope='session')
async def test_login_with_invalid_credentials() -> None:
    """
    誤った資格情報でログインを試みた場合のテスト。
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost:8000/") as client:
        response = await client.post(
            "/auth/login",
            data={"username": "wronguser@example.com", "password": "wrongpassword"},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        assert response.status_code == 401
        assert "Invalid email or password" in response.json()["detail"]

@pytest.mark.asyncio(loop_scope='session')
async def test_reset_password(authenticated_client: AsyncClient, db_session: AsyncSession) -> None:
    """
    パスワードリセットのテスト。
    """
    new_password = "newpassword"
    response = await authenticated_client.post(
        "/auth/reset-password",
        json={"email": TestData.TEST_USER_EMAIL_1, "new_password": new_password},
    )
    assert response.status_code == 200
    assert response.json()["msg"] == "Password reset successful"

    # データベース内のユーザーのパスワードを確認
    result = await db_session.execute(
        select(User).where(User.email == TestData.TEST_USER_EMAIL_1)
    )
    user: Optional[User] = result.scalars().first()
    assert user is not None
    assert verify_password(new_password, user.hashed_password)

@pytest.mark.asyncio(loop_scope='session')
async def test_reset_password_with_invalid_email(authenticated_client: AsyncClient, db_session: AsyncSession) -> None:
    """
    存在しないメールアドレスでパスワードリセットを試みた場合のテスト。
    """
    response = await authenticated_client.post(
        "/auth/reset-password",
        json={"email": "nonexistent@example.com", "new_password": "newpassword"},
    )
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"]