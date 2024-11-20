from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from app.database import get_db
from app.services.auth_service import authenticate_user, create_access_token, create_user, reset_password, get_current_user
from app.schema.user import UserCreate, PasswordReset, UserResponse
from app.core.config import settings
from fastapi.security import OAuth2PasswordBearer
from app.core.security import oauth2_scheme

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
    # 現在のユーザーを取得
    user = await get_current_user(token, db)
    return user

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
    # ユーザー作成ロジックを呼び出し
    new_user = await create_user(user.email, user.username, user.password, db)
    return {"msg": "User created successfully", "user_id": new_user.user_id}

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
    # ユーザー認証
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # アクセストークンを生成
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    """
    ログアウト処理を行うエンドポイント。

    Args:
        token (str): OAuth2トークン。

    Returns:
        dict: ログアウト成功メッセージ。
    """
    # クライアント側でトークンを削除する
    return {"msg": "Logged out successfully"}

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
    # パスワードリセットロジックを呼び出し
    await reset_password(data.email, data.new_password, db)
    return {"msg": "Password reset successful"}
