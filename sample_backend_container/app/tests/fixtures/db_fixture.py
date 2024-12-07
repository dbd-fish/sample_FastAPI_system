
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app.database import Base, configure_database
from main import app


@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_test_db():
    """テスト環境をセットアップするフィクスチャ。
    各テストごとにデータベースを初期化し、必要なシードデータを挿入します。
    """
    print("テスト環境のセットアップを開始")
    # テスト用データベースの設定
    db_config = configure_database(test_env=1)
    print(f"使用するデータベースURL: {db_config['database'].url}")

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost:8000") as client:
        # データベースの初期化 (clear_data API の呼び出し)
        print("テスト用データのクリアを開始")
        clear_response = await client.post("/dev/clear_data")
        print(clear_response)
        assert clear_response.status_code == 200

        # 必要なデータの挿入 (seed_data API の呼び出し)
        print("テスト用シードデータの挿入を開始")
        seed_response = await client.post("/dev/seed_data")
        print(seed_response)
        assert seed_response.status_code == 200

        print("テスト環境のセットアップを完了")

    yield  # テストの実行を許可
    # テストデータの後片付け
    async with db_config["engine"].begin() as conn:
        print("テスト後のデータ削除を開始")
        await conn.run_sync(Base.metadata.drop_all)

# @pytest_asyncio.fixture(scope="function")
# async def db_session() -> AsyncGenerator[AsyncSession, None]:
#     """
#     テスト用のデータベースセッションを提供するフィクスチャ。
#     """
#     async for session in get_db():
#     yield session
#     await session.close()
