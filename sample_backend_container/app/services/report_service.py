from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from app.models.report import Report
from app.schema.report import RequestReport, ResponseReport
from uuid import UUID
from app.core.config import TestData
from app.common.common import datetime_now
import structlog

# ログ設定
logger = structlog.get_logger()

async def create_report(report_data: RequestReport, db: AsyncSession) -> ResponseReport:
    """
    新しいレポートを作成するサービス関数。

    Args:
        report_data (RequestReport): 作成するレポートのデータ。
        db (AsyncSession): データベースセッション。

    Returns:
        ResponseReport: 作成されたレポートデータ (Pydanticスキーマ)。

    Raises:
        HTTPException: データベースエラーが発生した場合。
    """
    logger.info("create_report - start", report_data=report_data)
    new_report = Report(
        user_id=TestData.TEST_USER_ID_1,
        title=report_data.title,
        content=report_data.content,
        format=report_data.format,
        visibility=report_data.visibility,
    )
    try:
        db.add(new_report)
        await db.commit()
        await db.refresh(new_report)
        logger.info("create_report - success", report_id=new_report.report_id)
        return ResponseReport.model_validate(new_report)
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error("create_report - error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        logger.info("create_report - end")

async def update_report(report_id: str, updated_data: RequestReport, db: AsyncSession) -> ResponseReport:
    """
    レポートを更新するサービス関数。

    Args:
        report_id (str): 更新対象のレポートID。
        updated_data (RequestReport): 更新データ。
        db (AsyncSession): データベースセッション。

    Returns:
        ResponseReport: 更新されたレポートデータ (Pydanticスキーマ)。

    Raises:
        HTTPException: レポートが見つからない場合、またはデータベースエラーが発生した場合。
    """
    logger.info("update_report - start", report_id=report_id, updated_data=updated_data)
    report = await db.get(Report, UUID(report_id))
    if not report:
        logger.warning("update_report - report not found", report_id=report_id)
        raise HTTPException(status_code=404, detail="Report not found")

    for key, value in updated_data.model_dump(exclude_unset=True).items():
        setattr(report, key, value)
    try:
        await db.commit()
        await db.refresh(report)
        logger.info("update_report - success", report_id=report.report_id)
        return ResponseReport.model_validate(report)
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error("update_report - error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        logger.info("update_report - end")

async def delete_report(report_id: str, db: AsyncSession) -> dict:
    """
    レポートを論理削除するサービス関数。

    Args:
        report_id (str): 削除対象のレポートID。
        db (AsyncSession): データベースセッション。

    Returns:
        dict: 削除成功メッセージ。

    Raises:
        HTTPException: レポートが見つからない場合、またはデータベースエラーが発生した場合。
    """
    logger.info("delete_report - start", report_id=report_id)
    stmt = select(Report).where(Report.report_id == UUID(report_id), Report.deleted_at.is_(None))
    result = await db.execute(stmt)
    report = result.scalar_one_or_none()

    if not report:
        logger.warning("delete_report - report not found", report_id=report_id)
        raise HTTPException(status_code=404, detail="Report not found")

    report.deleted_at = datetime_now()
    try:
        await db.commit()
        logger.info("delete_report - success", report_id=report.report_id)
        return {"message": "Report deleted successfully"}
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error("delete_report - error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        logger.info("delete_report - end")

async def get_report_by_id_service(report_id: str, db: AsyncSession) -> ResponseReport:
    """
    指定されたIDのレポートを取得するサービス関数。

    Args:
        report_id (str): 取得対象のレポートID。
        db (AsyncSession): データベースセッション。

    Returns:
        ResponseReport: レポートデータ (Pydanticスキーマ)。

    Raises:
        HTTPException: レポートが見つからない場合。
    """
    logger.info("get_report_by_id_service - start", report_id=report_id)
    report = await db.get(Report, UUID(report_id))
    if not report:
        logger.warning("get_report_by_id_service - report not found", report_id=report_id)
        raise HTTPException(status_code=404, detail="Report not found")
    logger.info("get_report_by_id_service - success", report_id=report.report_id)
    logger.info("get_report_by_id_service - end")
    return ResponseReport.model_validate(report)
