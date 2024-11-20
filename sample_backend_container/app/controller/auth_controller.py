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
    ログインユーザー情報取得エンドポイント
    """
    user = await get_current_user(token, db)
    return user

@router.post("/register", response_model=dict)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    新規ユーザー登録エンドポイント
    """
    new_user = await create_user(user.email, user.username, user.password, db)
    return {"msg": "User created successfully", "user_id": new_user.user_id}

@router.post("/login", response_model=dict)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    """
    ログインエンドポイント
    """
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
@router.post("/logout")

async def logout(token: str = Depends(oauth2_scheme)):
    """
    ログアウト処理
    - クライアント側でトークンを削除するだけのシンプルな実装
    """
    # クライアントに対してログアウト成功を通知
    return {"msg": "Logged out successfully"}

@router.post("/reset-password", response_model=dict)
async def reset_password_endpoint(data: PasswordReset, db: AsyncSession = Depends(get_db)):
    """
    パスワードリセットエンドポイント
    """
    await reset_password(data.email, data.new_password, db)
    return {"msg": "Password reset successful"}
