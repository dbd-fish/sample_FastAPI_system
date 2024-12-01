import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.core.security import verify_password
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

@pytest_asyncio.fixture(scope="session", autouse=True)
def setup_test_logging():
    """
    pytestの実行時にログ出力をテスト用に切り替える。
    """
    print("ログ出力をテスト用に切り替え")
    configure_logging(test_env=2)  # 結合テスト用
    yield
    print("ログ出力を本番用に切り替え")
    configure_logging(test_env=0)  # 本番環境用

@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_test_db():
    """
    pytest 実行時にデータベース設定をテスト用に切り替える。
    """
    global db_config
    db_config = configure_database(test_env=2)
    print("テスト用のデータベースに切り替え")
    print(f"使用するデータベースURL: {db_config['database'].url}")
    database = db_config["database"]

    await database.disconnect()  # 現在の接続を切断
    await database.connect()     # テスト用に再接続

    yield  # 後続のテスト実行を許可

    await database.disconnect()
    print("本番用のデータベースに戻す")
    db_config = configure_database(test_env=0)

@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_test_data():
    print("setup_test_data: テストデータの準備を開始します")
    async with db_config["engine"].begin() as conn:
        print(f"シード対象DB: {db_config['database'].url}")
        await clear_data()
        await seed_data()
    yield
    async with db_config["engine"].begin() as conn:
        print("setup_test_data: テストデータを削除します")
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    テスト用のデータベースセッションを提供するフィクスチャ。
    """
    async with AsyncSessionLocal() as session:
        yield session

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
            data={"username": "testuser@example.com", "password": "password"},
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
        json={"email": "testuser@example.com", "new_password": new_password},
    )
    assert response.status_code == 200
    assert response.json()["msg"] == "Password reset successful"

    # データベース内のユーザーのパスワードを確認
    result = await db_session.execute(
        select(User).where(User.email == "testuser@example.com")
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