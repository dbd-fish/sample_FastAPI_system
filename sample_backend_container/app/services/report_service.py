from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from app.models.report import Report
from app.schema.report import RequestReport, ResponseReport
from uuid import UUID
from app.core.config import TestData
from app.common.common import datetime_now

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
    # 新しいレポートのインスタンスを作成
    new_report = Report(
        user_id=TestData.TEST_USER_ID_1,
        title=report_data.title,
        content=report_data.content,
        format=report_data.format,
        visibility=report_data.visibility,
    )
    try:
        db.add(new_report)  # レポートをデータベースに追加
        await db.commit()  # コミットして保存
        await db.refresh(new_report)  # 更新されたデータを取得
        return ResponseReport.model_validate(new_report)  # Pydanticモデルに変換して返却
    except SQLAlchemyError as e:
        await db.rollback()  # エラー発生時にロールバック
        raise HTTPException(status_code=500, detail=str(e))

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
    # 指定されたIDのレポートを取得
    report = await db.get(Report, UUID(report_id))
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    # 更新データを適用
    for key, value in updated_data.model_dump(exclude_unset=True).items():
        setattr(report, key, value)
    try:
        await db.commit()  # コミットして保存
        await db.refresh(report)  # 更新されたデータを取得
        return ResponseReport.model_validate(report)  # Pydanticモデルに変換して返却
    except SQLAlchemyError as e:
        await db.rollback()  # エラー発生時にロールバック
        raise HTTPException(status_code=500, detail=str(e))

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
    # 論理削除対象のレポートを取得
    stmt = select(Report).where(Report.report_id == UUID(report_id), Report.deleted_at.is_(None))
    result = await db.execute(stmt)
    report = result.scalar_one_or_none()

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    # 論理削除: deleted_at フィールドを現在時刻に設定
    report.deleted_at = datetime_now()
    try:
        await db.commit()  # コミットして保存
        return {"message": "Report deleted successfully"}
    except SQLAlchemyError as e:
        await db.rollback()  # エラー発生時にロールバック
        raise HTTPException(status_code=500, detail=str(e))

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
    # 指定されたIDのレポートを取得
    report = await db.get(Report, UUID(report_id))
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return ResponseReport.model_validate(report)  # Pydanticモデルに変換して返却
