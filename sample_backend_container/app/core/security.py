from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.models.user import User
from app.database import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# 環境変数に適切に置き換える
SECRET_KEY = "your_secret_key_here"  # JWTの署名に使用する秘密鍵
ALGORITHM = "HS256"  # JWTの暗号化アルゴリズム
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # アクセストークンの有効期限（分単位）

# パスワード暗号化設定
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# トークンのエンドポイント（FastAPIのOAuth2PasswordBearerを使用）
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def hash_password(password: str) -> str:
    """
    パスワードをハッシュ化する。

    Args:
        password (str): プレーンパスワード。

    Returns:
        str: ハッシュ化されたパスワード。
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    プレーンパスワードとハッシュ化されたパスワードを比較して検証する。

    Args:
        plain_password (str): プレーンパスワード。
        hashed_password (str): ハッシュ化されたパスワード。

    Returns:
        bool: 検証結果（True: 一致, False: 不一致）。
    """
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    アクセストークンを作成する。

    Args:
        data (dict): トークンに含めるデータ（例: {"sub": ユーザー識別子}）。
        expires_delta (timedelta, optional): トークンの有効期限（デフォルトは30分）。

    Returns:
        str: 作成されたJWTアクセストークン。
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})  # 有効期限をペイロードに追加
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> dict:
    """
    アクセストークンをデコードしてペイロードを取得する。

    Args:
        token (str): デコード対象のJWTアクセストークン。

    Returns:
        dict: デコードされたペイロード情報。

    Raises:
        HTTPException: トークンが無効または不正な場合。
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  # トークンをデコード
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def authenticate_user(email: str, password: str, db: AsyncSession) -> User:
    """
    メールアドレスとパスワードを使用してユーザー認証を行う。

    Args:
        email (str): ユーザーのメールアドレス。
        password (str): プレーンパスワード。
        db (AsyncSession): データベースセッション。

    Returns:
        User: 認証に成功したユーザーオブジェクト。

    Raises:
        HTTPException: 認証に失敗した場合。
    """
    query = select(User).where(User.email == email)  # メールアドレスでユーザーを検索
    result = await db.execute(query)
    user = result.scalars().first()  # 検索結果を取得
    if not user or not verify_password(password, user.password_hash):  # パスワードを検証
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
