from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from app.models.user import User
from app.common.common import datetime_now
from app.core.security import verify_password, create_access_token, hash_password
from datetime import timedelta
from uuid import UUID
from app.schema.user import UserResponse

ACCESS_TOKEN_EXPIRE_MINUTES = 30


async def authenticate_user(email: str, password: str, db: AsyncSession) -> User:
    """
    ユーザー認証を行うサービス関数。

    :param email: ユーザーのメールアドレス
    :param password: プレーンパスワード
    :param db: データベースセッション
    :return: 認証されたユーザー
    """
    stmt = select(User).where(User.email == email)
    try:
        result = await db.execute(stmt)
        user = result.scalars().first()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    return user


async def login_user(email: str, password: str, db: AsyncSession) -> dict:
    """
    ログイン処理を行うサービス関数。

    :param email: ユーザーのメールアドレス
    :param password: プレーンパスワード
    :param db: データベースセッション
    :return: アクセストークンとトークンタイプ
    """
    user = await authenticate_user(email, password, db)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


async def logout_user() -> dict:
    """
    ログアウト処理を行うサービス関数。

    :return: ログアウト成功メッセージ
    """
    # トークンの無効化やセッション管理が必要な場合、ここで実装する
    return {"message": "Logged out successfully"}


async def create_user(email: str, username: str, password: str, db: AsyncSession) -> UserResponse:
    hashed_password = hash_password(password)
    new_user = User(
        email=email,
        username=username,
        password_hash=hashed_password,
        user_role=1,  # デフォルトでゲスト
        user_status=1,  # デフォルトでアクティブ
    )
    try:
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return UserResponse.from_orm(new_user)
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


async def reset_password(email: str, new_password: str, db: AsyncSession) -> dict:
    """
    ユーザーのパスワードをリセットするサービス関数。

    :param email: ユーザーのメールアドレス
    :param new_password: 新しいパスワード
    :param db: データベースセッション
    :return: パスワードリセット成功メッセージ
    """
    stmt = select(User).where(User.email == email)
    try:
        result = await db.execute(stmt)
        user = result.scalars().first()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.password_hash = hash_password(new_password)
    user.updated_at = datetime_now()

    try:
        await db.commit()
        await db.refresh(user)
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    return {"message": "Password reset successful"}
