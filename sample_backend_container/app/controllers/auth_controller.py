from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from app.database import get_db
from app.services.auth_service import create_user, get_current_user
from app.core.security import authenticate_user, reset_password, create_access_token
from app.schemas.user import UserCreate, PasswordReset, UserResponse
from app.core.security import oauth2_scheme
import structlog

# ログの設定
logger = structlog.get_logger()

router = APIRouter()

@router.get("/me", response_model=UserResponse)
async def get_me(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    """
    現在ログインしているユーザーの情報を取得するエンドポイント。

    Args:
        token (str): OAuth2トークン。
        db (AsyncSession): 非同期データベースセッション。

    Returns:
        UserResponse: ログイン中のユーザー情報。
    """
    logger.info("get_me - start", token=token)
    try:
        user = await get_current_user(token, db)  # 現在のユーザーを取得
        logger.info("get_me - success", user_id=user.user_id)
        return user
    except Exception as e:
        logger.error("get_me - error", error=str(e))
        raise e
    finally:
        logger.info("get_me - end")

@router.post("/register", response_model=dict)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    新しいユーザーを登録するエンドポイント。

    Args:
        user (UserCreate): 新規ユーザーの情報（メール、ユーザー名、パスワード）。
        db (AsyncSession): 非同期データベースセッション。

    Returns:
        dict: 登録成功メッセージと新規ユーザーID。
    """
    logger.info("register_user - start", email=user.email, username=user.username)
    try:
        new_user = await create_user(user.email, user.username, user.password, db)
        logger.info("register_user - success", user_id=new_user.user_id)
        return {"msg": "User created successfully", "user_id": new_user.user_id}
    except Exception as e:
        logger.error("register_user - error", error=str(e))
        raise e
    finally:
        logger.info("register_user - end")

@router.post("/login", response_model=dict)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    """
    ログイン処理を行うエンドポイント。

    Args:
        form_data (OAuth2PasswordRequestForm): ユーザー名とパスワード。
        db (AsyncSession): 非同期データベースセッション。

    Returns:
        dict: アクセストークンとトークンタイプ。
    """
    logger.info("login - start", username=form_data.username)
    try:
        user = await authenticate_user(form_data.username, form_data.password, db)
        if not user:
            logger.warning("login - authentication failed", username=form_data.username)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = create_access_token(data={"sub": user.email})  # アクセストークンを生成
        logger.info("login - success", user_id=user.user_id)
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        logger.error("login - error", error=str(e))
        raise e
    finally:
        logger.info("login - end")

@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    """
    ログアウト処理を行うエンドポイント。

    Args:
        token (str): OAuth2トークン。

    Returns:
        dict: ログアウト成功メッセージ。
    """
    logger.info("logout - start", token=token)
    try:
        # クライアント側でトークンを削除するシンプルな処理
        logger.info("logout - success")
        return {"msg": "Logged out successfully"}
    except Exception as e:
        logger.error("logout - error", error=str(e))
        raise e
    finally:
        logger.info("logout - end")

@router.post("/reset-password", response_model=dict)
async def reset_password_endpoint(data: PasswordReset, db: AsyncSession = Depends(get_db)):
    """
    パスワードリセット処理を行うエンドポイント。

    Args:
        data (PasswordReset): パスワードリセットの情報（メールと新しいパスワード）。
        db (AsyncSession): 非同期データベースセッション。

    Returns:
        dict: パスワードリセット成功メッセージ。
    """
    logger.info("reset_password - start", email=data.email)
    try:
        await reset_password(data.email, data.new_password, db)
        logger.info("reset_password - success", email=data.email)
        return {"msg": "Password reset successful"}
    except Exception as e:
        logger.error("reset_password - error", error=str(e))
        raise e
    finally:
        logger.info("reset_password - end")
