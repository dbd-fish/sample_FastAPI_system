from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.models.user import User
from app.database import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status

# 環境変数に適切に置き換える
SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# パスワード暗号化
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# パスワードのハッシュ化
def hash_password(password: str) -> str:
    """
    パスワードをハッシュ化する。

    :param password: プレーンパスワード
    :return: ハッシュ化されたパスワード
    """
    return pwd_context.hash(password)

# パスワードの検証
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    プレーンパスワードとハッシュ化されたパスワードを検証する。

    :param plain_password: プレーンパスワード
    :param hashed_password: ハッシュ化されたパスワード
    :return: 検証結果（True: 一致, False: 不一致）
    """
    return pwd_context.verify(plain_password, hashed_password)

# アクセストークンの作成
def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    アクセストークンを作成する。

    :param data: トークンに含めるデータ
    :param expires_delta: トークンの有効期限
    :return: 作成されたJWTアクセストークン
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# アクセストークンのデコード
def decode_access_token(token: str) -> dict:
    """
    アクセストークンをデコードする。

    :param token: デコードするJWTアクセストークン
    :return: デコードされたペイロード情報
    :raises HTTPException: トークンが無効な場合に例外を発生
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

# ユーザー認証
async def authenticate_user(email: str, password: str, db: AsyncSession) -> User:
    """
    ユーザー認証を行う。

    :param email: ユーザーのメールアドレス
    :param password: プレーンパスワード
    :param db: データベースセッション
    :return: 認証に成功したユーザー
    """
    query = select(User).where(User.email == email)
    result = await db.execute(query)
    user = result.scalars().first()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    return user
