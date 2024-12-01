import pytest
import pytest_asyncio
from app.database import configure_database, Base, engine, AsyncSessionLocal
from app.core.log_config import configure_logging
from app.seeders.seed_data import clear_data, seed_data
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate
from app.models.user import User
from passlib.context import CryptContext
from app.services.auth_service import get_current_user
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from typing import Optional
from sqlalchemy import select
from main import app

@pytest_asyncio.fixture(scope="function")
def regist_user_data() -> UserCreate:
    """
    テスト用ユーザーデータの準備。
    """
    return UserCreate(
        email="registuser@example.com",
        username="registuser",
        password="password",
        user_role=2,
        user_status=1,
    )


@pytest_asyncio.fixture(scope="function")
async def authenticated_client() -> AsyncGenerator[AsyncClient, None]:
    """
    認証済みのクライアントを提供するフィクスチャ。
    """
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    # モックユーザーを定義
    mock_user = User(
        user_id=1,
        email="testuser@example.com",
        username="testuser",
        hashed_password=pwd_context.hash("password"),  # 実際のハッシュ化されたパスワードを設定
        user_role=2,
        user_status=1,
    )

    # get_current_userのオーバーライド関数を定義
    async def override_get_current_user() -> User:
        return mock_user

    # 依存関係をオーバーライド
    app.dependency_overrides[get_current_user] = override_get_current_user

    # 認証済みのクライアントを作成
    client = AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost:8000/")

    yield client

    # テスト後にオーバーライドをクリア
    app.dependency_overrides.clear()
