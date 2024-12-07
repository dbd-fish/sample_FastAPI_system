from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.common.common import datetime_now
from app.models.report import Report


class ReportRepository:
    """レポートに関連するデータベース操作を担当するリポジトリクラス。"""

    @staticmethod
    async def create_report(db: AsyncSession, report: Report) -> Report:
        """レポートをデータベースに追加します。

        Args:
            db (AsyncSession): データベースセッション。
            report (Report): 追加するレポートオブジェクト。

        Returns:
            Report: 追加されたレポートオブジェクト。

        """
        db.add(report)
        await db.commit()
        await db.refresh(report)
        return report

    @staticmethod
    async def get_report_by_id(db: AsyncSession, report_id: UUID) -> Report | None:
        """指定されたIDのレポートを取得します。

        未削除のレポートのみ取得可能です。

        Args:
            db (AsyncSession): データベースセッション。
            report_id (UUID): レポートのID。

        Returns:
            Report | None: レポートオブジェクト、または該当なしの場合はNone。

        """
        stmt = (
            select(Report)
            .where(Report.report_id == report_id, Report.deleted_at.is_(None))
        )
        result = await db.execute(stmt)
        return result.scalars().first()

    @staticmethod
    async def update_report(db: AsyncSession, report: Report) -> Report:
        """指定されたレポートを更新します。

        未削除のレポートのみ更新可能です。

        Args:
            db (AsyncSession): データベースセッション。
            report (Report): 更新するレポートのデータを持つオブジェクト。

        Returns:
            Report | None: 更新後のレポートオブジェクト、または該当なしの場合はNone。

        """
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

    @staticmethod
    async def delete_report(db: AsyncSession, report: Report) -> None:
        """指定されたレポートを論理削除します。

        レポートの `deleted_at` フィールドを現在日時に設定します。

        Args:
            db (AsyncSession): データベースセッション。
            report (Report): 論理削除するレポートオブジェクト。

        """
        report.deleted_at = datetime_now()
        await db.commit()
        await db.refresh(report)

    @staticmethod
    async def fetch_report_for_update(db: AsyncSession, report_id: UUID) -> Report | None:
        """更新用にレポートを取得します。

        未削除のレポートのみ取得可能です。

        Args:
            db (AsyncSession): データベースセッション。
            report_id (UUID): レポートのID。

        Returns:
            Report | None: レポートオブジェクト、または該当なしの場合はNone。

        """
        stmt = select(Report).where(Report.report_id == report_id, Report.deleted_at.is_(None))
        result = await db.execute(stmt)
        return result.scalar_one_or_none()
