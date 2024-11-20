from pydantic import BaseModel

class Token(BaseModel):
    """
    トークン情報を表すモデル。
    """
    access_token: str  # アクセストークンの文字列
    token_type: str  # トークンの種類（通常は "bearer"）

class TokenData(BaseModel):
    """
    トークンに含まれるデータを表すモデル。
    """
    email: str | None = None  # トークンに関連付けられたメールアドレス（オプション）
