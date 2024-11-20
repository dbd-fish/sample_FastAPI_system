from datetime import datetime, timedelta
from fastapi import HTTPException, status
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.schema.user import UserCreate, UserResponse
from app.core.config import settings
from fastapi import Depends
from typing import Annotated
from app.core.security import oauth2_scheme
from pydantic import ValidationError
import structlog

# ログの初期化
logger = structlog.get_logger()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: AsyncSession):
    """
    現在のユーザーを取得する
    """
    logger.info("get_current_user - start", token=token)
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            logger.warning("get_current_user - token missing 'sub'", token=token)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        query = select(User).where(User.email == email)
        result = await db.execute(query)
        user = result.scalars().first()
        if user is None:
            logger.warning("get_current_user - user not found", email=email)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        logger.info("get_current_user - success", user_id=user.user_id)
        return UserResponse(
            user_id=user.user_id,
            email=user.email,
            username=user.username
        )

    except JWTError as e:
        logger.error("get_current_user - jwt decode error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except ValidationError as e:
        logger.error("get_current_user - validation error", errors=e.errors())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="User validation failed"
        )
    finally:
        logger.info("get_current_user - end")

def verify_password(plain_password, hashed_password):
    """
    パスワードを検証する
    """
    logger.info("verify_password - start")
    result = pwd_context.verify(plain_password, hashed_password)
    logger.info("verify_password - end", result=result)
    return result

def get_password_hash(password):
    """
    パスワードをハッシュ化する
    """
    logger.info("get_password_hash - start")
    hashed_password = pwd_context.hash(password)
    logger.info("get_password_hash - end")
    return hashed_password

def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    アクセストークンを生成する
    """
    logger.info("create_access_token - start")
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    logger.info("create_access_token - end", expire=expire)
    return encoded_jwt

async def authenticate_user(email: str, password: str, db: AsyncSession):
    """
    ユーザーをメールアドレスとパスワードで認証する
    """
    logger.info("authenticate_user - start", email=email)
    query = select(User).where(User.email == email)
    result = await db.execute(query)
    user = result.scalars().first()
    if not user:
        logger.warning("authenticate_user - user not found", email=email)
        logger.info("authenticate_user - end", success=False)
        return None
    if not verify_password(password, user.password_hash):
        logger.warning("authenticate_user - incorrect password", email=email)
        logger.info("authenticate_user - end", success=False)
        return None
    logger.info("authenticate_user - success", user_id=user.user_id)
    logger.info("authenticate_user - end", success=True)
    return user

async def create_user(email: str, username: str, password: str, db: AsyncSession):
    """
    新しいユーザーを作成する
    """
    logger.info("create_user - start", email=email, username=username)
    hashed_password = get_password_hash(password)
    new_user = User(
        email=email,
        username=username,
        password_hash=hashed_password,
        user_role=1,
        user_status=1,
    )
    try:
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        logger.info("create_user - success", user_id=new_user.user_id)
        return new_user
    except Exception as e:
        logger.error("create_user - error", error=str(e))
        await db.rollback()
        raise e
    finally:
        logger.info("create_user - end")

async def reset_password(email: str, new_password: str, db: AsyncSession):
    """
    パスワードをリセットする
    """
    logger.info("reset_password - start", email=email)
    query = select(User).where(User.email == email)
    result = await db.execute(query)
    user = result.scalars().first()

    if not user:
        logger.warning("reset_password - user not found", email=email)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    user.password_hash = get_password_hash(new_password)
    user.updated_at = datetime.utcnow()
    try:
        await db.commit()
        await db.refresh(user)
        logger.info("reset_password - success", user_id=user.user_id)
        return user
    except Exception as e:
        logger.error("reset_password - error", error=str(e))
        await db.rollback()
        raise e
    finally:
        logger.info("reset_password - end")
