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
from typing import Optional
from sqlalchemy import select
from main import app

@pytest_asyncio.fixture(scope="function", autouse=True)
def setup_test_logging():
    """
    pytestの実行時にログ出力をテスト用に切り替える。
    """
    print("ログ出力をテスト用に切り替え")
    configure_logging(test_env=1)  # 結合テスト用
    yield
    print("ログ出力を本番用に切り替え")
    configure_logging(test_env=0)  # 本番環境用
