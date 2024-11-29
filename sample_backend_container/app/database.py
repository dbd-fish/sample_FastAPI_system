import configparser
from databases import Database
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import AsyncGenerator

Base = declarative_base()

def get_database_url(test_env: int = 0) -> str:
    """
    環境に応じてデータベース接続URLを取得します。

    Args:
        test_env (int): 環境指定フラグ (0: 本番、1: 単体テスト、2: 結合テスト)。

    Returns:
        str: データベース接続URL。
    """
    if test_env == 1:
        return "postgresql+asyncpg://user:password@db:5432/ut_sample_db"
    elif test_env == 2:
        return "postgresql+asyncpg://user:password@db:5432/it_sample_db"
    else:
        config = configparser.ConfigParser()
        config.read("alembic.ini")
        return config.get("alembic", "sqlalchemy.url")


def configure_database(test_env: int = 0, echo: bool = True):
    """
    データベース接続とセッションを設定します。

    Args:
        test_env (int): 環境指定フラグ。
        echo (bool): SQLAlchemyのログ出力を有効化するか。

    Returns:
        dict: データベース、エンジン、セッション情報を含む辞書。
    """
    database_url = get_database_url(test_env)
    database = Database(database_url)
    engine = create_async_engine(database_url, echo=echo)
    async_session_local = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    return {
        "database": database,
        "engine": engine,
        "sessionmaker": async_session_local,
    }


# 本番環境のデフォルト設定
db_config = configure_database()
database = db_config["database"]
engine = db_config["engine"]
AsyncSessionLocal = db_config["sessionmaker"]

async def get_db() -> AsyncGenerator:
    """
    非同期データベースセッションを生成するジェネレーター関数。

    Yields:
        AsyncSession: 非同期セッションインスタンス。
    """
    async with AsyncSessionLocal() as session:
        yield session
