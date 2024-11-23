

from pydantic_settings import BaseSettings


class Setting(BaseSettings):
    # アプリケーション基本設定
    APP_NAME: str = "Sample FastAPI App"


    # セキュリティ設定
    SECRET_KEY: str = "your_secret_key_here"  # JWT署名用の秘密鍵
    ALGORITHM: str = "HS256"  # JWTアルゴリズム
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # アクセストークンの有効期限（分）

    APP_LOG_DIRECTORY: str  = "logs/app"
    SQL_LOG_DIRECTORY: str  = "logs/sql"

    # データベース設定
    # alembic.iniに記載



    class Config:
        env_file = ".env"  # .envファイルから環境変数を読み込む設定

setting = Setting()
