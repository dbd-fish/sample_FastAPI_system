

from pydantic_settings import BaseSettings

# 動作確認データ
class TestData:
    TEST_USER_ID_1 = "123e4567-e89b-12d3-a456-426614174000"
    TEST_USER_ID_2 = "223e4567-e89b-12d3-a456-426614174000"
    TEST_GROUP_ID = "223e4567-e89b-12d3-a456-426614174002"
    TEST_REPORT_ID = "323e4567-e89b-12d3-a456-426614174003"


class Settings(BaseSettings):
    # アプリケーション基本設定
    APP_NAME: str = "Sample FastAPI App"
    VERSION: str = "1.0.0"
    DEBUG: bool = True

    # セキュリティ設定
    SECRET_KEY: str = "your_secret_key_here"  # JWT署名用の秘密鍵
    ALGORITHM: str = "HS256"  # JWTアルゴリズム
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # アクセストークンの有効期限（分）

    # データベース設定
    # DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/sample_db"

    # メール関連の設定（例: パスワードリセットで使用する場合）
    SMTP_SERVER: str = "smtp.example.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = "your_email@example.com"
    SMTP_PASSWORD: str = "your_password"
    EMAIL_FROM: str = "your_email@example.com"
    EMAIL_FROM_NAME: str = "Sample App"

    class Config:
        env_file = ".env"  # .envファイルから環境変数を読み込む設定

settings = Settings()
