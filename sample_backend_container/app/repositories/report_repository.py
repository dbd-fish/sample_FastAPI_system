from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from uuid import UUID
from app.models.report import Report
from app.common.common import datetime_now
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import NoResultFound


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
        stmt = (
            select(Report)
            .where(Report.report_id == report_id, Report.deleted_at.is_(None))
        )
        result = await db.execute(stmt)
        return result.scalars().first()

    @staticmethod
    async def update_report(db: AsyncSession, report: Report) -> Report | None:
        """指定されたレポートを更新します。論理削除済みの場合は更新を行いません。"""
        try:
            # 論理削除されていないレポートを取得
            stmt = (
                select(Report)
                .where(Report.report_id == report.report_id, Report.deleted_at.is_(None))
            )
            result = await db.execute(stmt)
            existing_report = result.scalars().one()
            
            # 更新内容を適用
            existing_report.title = report.title
            existing_report.content = report.content
            existing_report.format = report.format
            existing_report.visibility = report.visibility
            
            await db.commit()
            await db.refresh(existing_report)
            return existing_report
        except NoResultFound:
            # レポートが存在しないか、論理削除されている場合
            return None

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
