from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from uuid import UUID
from app.models.report import Report
from app.common.common import datetime_now


class ReportRepository:
    """レポートに関連するデータベース操作を担当するリポジトリクラス。"""

    @staticmethod
    async def create_report(db: AsyncSession, report: Report) -> Report:
        """レポートをデータベースに追加します。"""
        db.add(report)
        await db.commit()
        await db.refresh(report)
        return report

    @staticmethod
    async def get_report_by_id(db: AsyncSession, report_id: UUID) -> Report | None:
        """指定されたIDのレポートを取得します。"""
        return await db.get(Report, report_id)

    @staticmethod
    async def update_report(db: AsyncSession, report: Report) -> Report:
        """指定されたレポートを更新します。"""
        await db.commit()
        await db.refresh(report)
        return report

    @staticmethod
    async def delete_report(db: AsyncSession, report: Report) -> None:
        """指定されたレポートを論理削除します。"""
        report.deleted_at = datetime_now()
        await db.commit()

    @staticmethod
    async def fetch_report_for_update(db: AsyncSession, report_id: UUID) -> Report | None:
        """更新用にレポートを取得します（未削除のもののみ）。"""
        stmt = select(Report).where(Report.report_id == report_id, Report.deleted_at.is_(None))
        result = await db.execute(stmt)
        return result.scalar_one_or_none()
