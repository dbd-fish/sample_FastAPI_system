from pydantic import BaseModel, EmailStr
from uuid import UUID

class UserCreate(BaseModel):
    """
    ユーザー作成時のリクエストデータを表すモデル。
    """
    email: EmailStr  # ユーザーのメールアドレス
    username: str  # ユーザー名
    password: str  # ユーザーのパスワード

class PasswordReset(BaseModel):
    """
    パスワードリセット時のリクエストデータを表すモデル。
    """
    email: EmailStr  # パスワードをリセットする対象のメールアドレス
    new_password: str  # 新しいパスワード

class UserResponse(BaseModel):
    """
    ユーザー情報のレスポンスデータを表すモデル。
    """
    user_id: UUID  # ユーザーの一意な識別子
    email: EmailStr  # ユーザーのメールアドレス
    username: str  # ユーザー名

    class Config:
        """
        Pydanticモデルの設定クラス。
        """
        from_attributes = True  # モデルの属性からデータを生成可能にする
