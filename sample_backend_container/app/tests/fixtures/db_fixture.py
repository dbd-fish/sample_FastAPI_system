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
