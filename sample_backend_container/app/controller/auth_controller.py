from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.auth_service import login_user, logout_user, create_user, reset_password
from app.schema.user import UserCreate, UserLogin, PasswordReset, UserResponse
from app.core.security import decode_access_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    ユーザー登録エンドポイント
    """
    new_user = await create_user(user.email, user.username, user.password, db)
    return new_user


@router.post("/login", response_model=dict)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    """
    ログインエンドポイント
    usernameはemailとする
    """
    token_data = await login_user(form_data.username, form_data.password, db)
    return token_data


@router.post("/logout", response_model=dict)
async def logout():
    """
    ログアウトエンドポイント
    """
    result = await logout_user()
    return result


@router.post("/reset-password", response_model=dict)
async def reset_password_endpoint(data: PasswordReset, db: AsyncSession = Depends(get_db)):
    """
    パスワードリセットエンドポイント
    """
    message = await reset_password(data.email, data.new_password, db)
    return message
