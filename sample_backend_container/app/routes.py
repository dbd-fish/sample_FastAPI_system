from fastapi import APIRouter

from app.config.setting import setting
from app.controllers.auth_controller import router as auth_router
from app.controllers.dev_controller import router as dev_router
from app.controllers.report_controller import router as report_router

router = APIRouter()

if setting.DEV_MODE:
    # 開発用のルーター定義
    router.include_router(dev_router, prefix="/dev",  tags=["dev"])

# レポート用のルーター定義
router.include_router(report_router, prefix="/report",  tags=["report"])

# 認証用のルーター
router.include_router(auth_router, prefix="/auth", tags=["auth"])
