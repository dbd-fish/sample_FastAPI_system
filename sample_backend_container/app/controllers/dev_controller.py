from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.report import RequestReport, ResponseReport
from app.schemas.user import UserResponse
from app.services.report_service import create_report, update_report, delete_report, get_report_by_id_service
from app.models.user import User
import structlog
from app.services.auth_service import get_current_user
from app.seeders.seed_data import clear_data, seed_data

# ロガーの設定
logger = structlog.get_logger()

router = APIRouter()


@router.post("/clear_data", response_model=dict)
async def clear_data_endpoint(
    db: AsyncSession = Depends(get_db),
):
    """
    【開発用】
    全テーブルのクリア処理

    Args:
        db (AsyncSession): データベースセッション。

    Returns:
        dict: 成功メッセージ
    """
    logger.info("clear_data_endpoint - start")
    try:
        await clear_data() 
        logger.info("clear_data_endpoint - success")
        return   {"msg": "clear_data API successfully"}
    finally:
        logger.info("clear_data_endpoint - end")

@router.post("/seed_data", response_model=dict)
async def seed_data_endpoint(
    db: AsyncSession = Depends(get_db),
):
    """
    【開発用】
    全テーブルのシーダー処理
    Args:
        db (AsyncSession): データベースセッション。

    Returns:
        dict: 成功メッセージ
    """
    logger.info("seed_data_endpoint - start")
    try:
        await seed_data() 
        logger.info("seed_data_endpoint - success")
        return  {"msg": "seed_data API successfully"}
    finally:
        logger.info("seed_data_endpoint - end")
