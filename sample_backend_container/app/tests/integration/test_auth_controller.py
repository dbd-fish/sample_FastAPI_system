import pytest
from httpx import AsyncClient, ASGITransport
from main import app
from app.database import Base, engine
from app.schemas.user import UserCreate
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import create_access_token
from app.seeders.seed_data import clear_data, seed_data
from app.config.test_data import TestData
from app.core.log_config import configure_logging

@pytest.fixture(scope="session", autouse=True)
def setup_test_logging():
    """
    pytestの実行時にログ出力をテスト用に切り替え、終了時に元に戻す。
    """
    # pytest開始時にログをテスト用に切り替える
    configure_logging(test_env=2)  # 結合テスト用
    yield
    # pytest終了後にログを通常用に切り替える
    configure_logging(test_env=0)  # 本番環境用

@pytest.fixture(scope="function", autouse=True)
async def setup_db():
    """
    テスト用のデータベースをセットアップします。
    """
    async with engine.begin() as conn:
        # 確実にテーブルを作成
            await clear_data()
            await seed_data()
    yield
    async with engine.begin() as conn:
        # 確実にテーブルを削除
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="session", autouse=True)
async def cleanup_database_at_session_end():
    """テストセッション終了時にデータベースをクリアします。"""
    yield
    await clear_data()

@pytest.fixture(scope="function")
def regist_user_data():
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


# @pytest.fixture(scope="function")
# async def test_user(test_user_data):
#     """
#     テスト用ユーザーをデータベースに追加。
#     """
#     async with AsyncSession(engine) as session:
#         user = User(
#             email=test_user_data.email,
#             username=test_user_data.username,
#             password_hash="hashedpassword",  # 仮のハッシュ値
#             user_status=test_user_data.user_status,
#             user_role=test_user_data.user_role,
#         )
#         session.add(user)
#         await session.commit()
#         await session.refresh(user)
#         return user


@pytest.mark.asyncio
async def test_register_user(regist_user_data):
    """
    ユーザー登録のテスト。
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost:8000/") as client:
        response = await client.post("/auth/register", json=regist_user_data.model_dump())
        assert response.status_code == 200
        assert response.json()["msg"] == "User created successfully"


@pytest.mark.asyncio
async def test_login_user(test_user_data):
    """
    ログイン処理のテスト。
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost:8000/") as client:
        response = await client.post(
            "/auth/login",
            data={"username": "testuser@example.com", "password": "password"},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        assert response.status_code == 200
        assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_get_me(test_user):
    """
    現在ログイン中のユーザー情報取得のテスト。
    """
    user = await test_user  # 明示的に await
    token = create_access_token({"sub": user.email})
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost:8000/") as client:
        response = await client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
        assert response.json()["email"] == user.email


@pytest.mark.asyncio
async def test_reset_password(test_user):
    """
    パスワードリセットのテスト。
    """
    user = await test_user  # 明示的に await
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost:8000/") as client:
        response = await client.post(
            "/auth/reset-password",
            json={"email": user.email, "new_password": "newpassword"},
        )
        assert response.status_code == 200
        assert response.json()["msg"] == "Password reset successful"
