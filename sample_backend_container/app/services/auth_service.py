from fastapi import HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.repositories.auth_repository import UserRepository
from app.schemas.user import UserResponse
from app.config.setting import setting
from app.core.security import oauth2_scheme, hash_password
from jose import jwt, JWTError
from pydantic import ValidationError
from typing import Annotated
import structlog
from app.database import get_db

logger = structlog.get_logger()


# TODO: なぜこれでいけるのかしらべる。1リクエスト内に複数のDepends(get_db)が存在する場合、FastAPIが再利用してくれる？？
async def get_current_user(
    db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> UserResponse:
    """
    トークンから現在のユーザーを取得します。

    トークンをデコードして、その情報をもとにデータベースからユーザーを取得します。
    トークンが無効、またはユーザーが存在しない場合は例外をスローします。

    Args:
        token (Annotated[str, Depends]): Bearerトークン。
        db (AsyncSession): 非同期データベースセッション。

    Returns:
        UserResponse: 現在のユーザー情報（Pydanticスキーマ形式）。

    Raises:
        HTTPException:
            - 401: トークンが無効または`sub`フィールドが存在しない場合。
            - 404: ユーザーが存在しない場合。
            - 500: バリデーションエラーが発生した場合。
    """
    logger.info("get_current_user - start", token=token)
    try:
        # トークンをデコードしてペイロードを取得
        payload = jwt.decode(token, setting.SECRET_KEY, algorithms=[setting.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            logger.warning("get_current_user - token missing 'sub'", token=token)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # ユーザーをデータベースから取得
        user = await UserRepository.get_user_by_email(db, email)
        if user is None:
            logger.warning("get_current_user - user not found", email=email)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        logger.info("get_current_user - success", user_id=user.user_id)
        return UserResponse(
            user_id=user.user_id,
            email=user.email,
            username=user.username,
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
            detail="User validation failed",
        )
    finally:
        logger.info("get_current_user - end")


async def create_user(
    email: str, username: str, password: str, db: AsyncSession
) -> User:
    """
    新しいユーザーを作成します。

    ユーザーの情報をもとに新しいユーザーをデータベースに登録します。
    パスワードはハッシュ化されて保存されます。
    エラーが発生した場合はロールバックし、例外をスローします。

    Args:
        email (str): ユーザーのメールアドレス。
        username (str): ユーザー名。
        password (str): プレーンテキストのパスワード。
        db (AsyncSession): 非同期データベースセッション。

    Returns:
        User: 作成されたユーザーオブジェクト。

    Raises:
        HTTPException: ユーザー作成中に発生したエラー。
    """
    logger.info("create_user - start", email=email, username=username)

    # パスワードをハッシュ化
    hashed_password = hash_password(password)

    # 新しいユーザーオブジェクトを作成
    new_user = User(
        email=email,
        username=username,
        password_hash=hashed_password,
        user_role=1,
        user_status=1,
    )

    try:
        # データベースにユーザーを保存
        saved_user = await UserRepository.create_user(db, new_user)
        logger.info("create_user - success", user_id=saved_user.user_id)
        return saved_user
    except Exception as e:
        logger.error("create_user - error", error=str(e))
        raise HTTPException(status_code=500, detail="User creation failed")
    finally:
        logger.info("create_user - end")
