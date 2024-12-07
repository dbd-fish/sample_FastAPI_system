from uuid import UUID

import structlog
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.report import Report
from app.repositories.report_repository import ReportRepository
from app.schemas.report import RequestReport, ResponseReport
from app.schemas.user import UserResponse

logger = structlog.get_logger()

async def create_report(report_data: RequestReport, current_user: UserResponse, db: AsyncSession) -> ResponseReport:
    """新しいレポートを作成するサービス関数。

    Args:
        report_data (RequestReport): 作成するレポートのデータ。
        current_user (UserResponse): 現在ログインしているユーザー情報。
        db (AsyncSession): データベースセッション。

    Returns:
        ResponseReport: 作成されたレポートのレスポンスモデル。

    Raises:
        HTTPException: データベースエラーまたはその他のエラーが発生した場合。

    """
    logger.info("create_report - start", report_data=report_data)

    try:
        new_report = Report(
            user_id=current_user.user_id,
            title=report_data.title,
            content=report_data.content,
            format=report_data.format,
            visibility=report_data.visibility,
        )
        saved_report = await ReportRepository.create_report(db, new_report)
        logger.info("create_report - success", report_id=saved_report.report_id)
        result =  ResponseReport.model_validate(saved_report)
        return result
    finally:
        logger.info("create_report - end")

async def update_report(report_id: str, updated_data: RequestReport, db: AsyncSession) -> ResponseReport:
    """レポートを更新するサービス関数。

    Args:
        report_id (str): 更新するレポートのID。
        updated_data (RequestReport): 更新内容を含むデータ。
        db (AsyncSession): データベースセッション。

    Returns:
        ResponseReport: 更新されたレポートのレスポンスモデル。

    Raises:
        HTTPException: レポートが見つからない場合、またはデータベースエラーが発生した場合。

    """
    logger.info("update_report - start", report_id=report_id, updated_data=updated_data)

    report = await ReportRepository.get_report_by_id(db, UUID(report_id))
    if not report:
        logger.warning("update_report - report not found", report_id=report_id)
        raise HTTPException(status_code=404, detail="Report not found")

    for key, value in updated_data.model_dump(exclude_unset=True).items():
        setattr(report, key, value)

    try:
        updated_report = await ReportRepository.update_report(db, report)
        logger.info("update_report - success", report_id=updated_report.report_id)
        return ResponseReport.model_validate(updated_report)
    finally:
        logger.info("update_report - end")

async def delete_report(report_id: str, db: AsyncSession) -> dict:
    """レポートを論理削除するサービス関数。

    Args:
        report_id (str): 削除対象のレポートのID。
        db (AsyncSession): データベースセッション。

    Returns:
        dict: 削除成功のメッセージ。

    Raises:
        HTTPException: レポートが見つからない場合、またはデータベースエラーが発生した場合。

    """
    logger.info("delete_report - start", report_id=report_id)

    report = await ReportRepository.fetch_report_for_update(db, UUID(report_id))
    if not report:
        logger.warning("delete_report - report not found", report_id=report_id)
        raise HTTPException(status_code=404, detail="Report not found")

    try:
        await ReportRepository.delete_report(db, report)
        logger.info("delete_report - success", report_id=report.report_id)
        return {"msg": "Report deleted successfully"}
    finally:
        logger.info("delete_report - end")

async def get_report_by_id_service(report_id: str, db: AsyncSession) -> ResponseReport:
    """指定されたIDのレポートを取得するサービス関数。

    Args:
        report_id (str): 取得対象のレポートのID。
        db (AsyncSession): データベースセッション。

    Returns:
        ResponseReport: 取得したレポートのレスポンスモデル。

    Raises:
        HTTPException: レポートが見つからない場合、またはその他のエラーが発生した場合。

    """
    logger.info("get_report_by_id_service - start", report_id=report_id)

    report = await ReportRepository.get_report_by_id(db, UUID(report_id))
    if not report:
        logger.warning("get_report_by_id_service - not found", report_id=report_id)
        raise HTTPException(status_code=404, detail="Report not found")

    try:
        logger.info("get_report_by_id_service - success", report_id=report.report_id)
        return ResponseReport.model_validate(report)
    finally:
        logger.info("get_report_by_id_service - end")
