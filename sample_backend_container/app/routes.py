from fastapi import APIRouter
from app.controller.report_controller import router as report_router
from app.controller.auth_controller import router as auth_router

router = APIRouter()

# レポート用のルーター定義  
router.include_router(report_router, prefix="")

# 認証用のルーター
router.include_router(auth_router, prefix="/auth", tags=["Authentication"])