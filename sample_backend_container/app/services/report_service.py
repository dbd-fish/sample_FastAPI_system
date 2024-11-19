from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from app.models.report import Report
from app.schema.report import RequestReport
from uuid import UUID
from app.config.config import TestData
from app.common.common import datetime_now

async def create_report(report_data: RequestReport, db: AsyncSession) -> Report:
    """
    新しいレポートを作成するサービス関数。

    :param report_data: 作成するレポートのデータ
    :param db: データベースセッション
    :return: 作成されたレポート
    """
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
        return new_report
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

async def update_report(report_id: str, updated_data: RequestReport, db: AsyncSession) -> Report:
    """
    レポートを更新するサービス関数。

    :param report_id: 更新対象のレポートID
    :param updated_data: 更新するデータ
    :param db: データベースセッション
    :return: 更新されたレポート
    """
    report = await db.get(Report, UUID(report_id))
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    for key, value in updated_data.model_dump(exclude_unset=True).items():
        setattr(report, key, value)
    try:
        await db.commit()
        await db.refresh(report)
        return report
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

async def delete_report(report_id: str, db: AsyncSession):
    """
    レポートを論理削除するサービス関数。
    """
    stmt = select(Report).where(Report.report_id == UUID(report_id), Report.deleted_at.is_(None))
    result = await db.execute(stmt)
    report = result.scalar_one_or_none()

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    # 論理削除: deleted_at を現在時刻に設定
    report.deleted_at = datetime_now()
    try:
        await db.commit()
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

async def get_report_by_id_service(report_id: str, db: AsyncSession) -> Report:
    """
    指定されたIDのレポートを取得するサービス関数。

    :param report_id: 取得対象のレポートID
    :param db: データベースセッション
    :return: レポートオブジェクト
    """
    report = await db.get(Report, UUID(report_id))
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report
