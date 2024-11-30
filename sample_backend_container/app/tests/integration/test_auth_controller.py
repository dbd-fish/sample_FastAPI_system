import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from main import app
from app.database import configure_database, Base
from app.schemas.user import UserCreate
from app.core.log_config import configure_logging
from app.seeders.seed_data import clear_data, seed_data
from app.services.auth_service import get_current_user
from app.models.user import User
from passlib.context import CryptContext

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

@pytest_asyncio.fixture(scope="function")
def authenticated_client():
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
    async def override_get_current_user():
        return mock_user

    # 依存関係をオーバーライド
    app.dependency_overrides[get_current_user] = override_get_current_user

    # 認証済みのクライアントを作成
    client = AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost:8000/")

    yield client

    # テスト後にオーバーライドをクリア
    app.dependency_overrides.clear()

@pytest.mark.asyncio(loop_scope='session')
async def test_register_user(regist_user_data):
    """
    ユーザー登録のテスト。
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost:8000/") as client:
        response = await client.post("/auth/register", json=regist_user_data.model_dump())
        assert response.status_code == 200
        assert response.json()["msg"] == "User created successfully"

@pytest.mark.asyncio(loop_scope='session')
async def test_login_user():
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
async def test_reset_password(authenticated_client):
    """
    パスワードリセットのテスト。
    """
    response = await authenticated_client.post(
        "/auth/reset-password",
        json={"email": "testuser@example.com", "new_password": "newpassword"},
    )
    assert response.status_code == 200
    assert response.json()["msg"] == "Password reset successful"
