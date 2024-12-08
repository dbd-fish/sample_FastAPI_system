

from pydantic_settings import BaseSettings


class Setting(BaseSettings):
    # アプリケーション基本設定
    APP_NAME: str = "Sample FastAPI App"

    # 開発モード
    DEV_MODE: bool = True

    # セキュリティ設定
    SECRET_KEY: str = "your_secret_key_here"  # JWT署名用の秘密鍵
    ALGORITHM: str = "HS256"  # JWTアルゴリズム
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # アクセストークンの有効期限（分）

    # ログの保存先
    APP_LOG_DIRECTORY: str  = "logs/server/app"
    SQL_LOG_DIRECTORY: str  = "logs/server/sql"
    PYTEST_APP_LOG_DIRECTORY: str  = "logs/Pytest/app"
    PYTEST_SQL_LOG_DIRECTORY: str  = "logs/Pytest/sql"


    # データベース設定
    # alembic.iniに記載


setting = Setting()
