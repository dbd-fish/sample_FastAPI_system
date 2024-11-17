import configparser
from databases import Database

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import AsyncGenerator
# alembic.iniファイルからDB接続
config = configparser.ConfigParser()
config.read('alembic.ini')  # alembic.iniのパスは適宜調整
DATABASE_URL = config.get('alembic', 'sqlalchemy.url')
# Databasesパッケージの設定
database = Database(DATABASE_URL)

# 非同期セッションの設定
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    bind=engine,  # 非同期エンジンをバインド
    class_=AsyncSession,  # 非同期セッションを指定
    expire_on_commit=False  # コミット後にオブジェクトが有効であることを保証
)
Base = declarative_base()

# データベースセッションの依存関係を提供する関数
# FastAPIのエンドポイントで使用される
async def get_db() -> AsyncGenerator:
    """
    非同期データベースセッションを生成するジェネレーター関数。
    エンドポイント内でこの関数を使用してセッションを取得。

    :yield: 非同期セッションインスタンス
    """
    async with AsyncSessionLocal() as session:
        yield session