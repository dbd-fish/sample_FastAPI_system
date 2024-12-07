import uuid
from datetime import datetime

from sqlalchemy import TIMESTAMP, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.common.common import datetime_now
from app.database import Base


# ReportViewHistoryモデル: レポート閲覧履歴テーブル
class ReportViewHistory(Base):
    __tablename__ = "report_view_history"

    # 履歴ID - プライマリキー、自動インクリメント
    history_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="履歴ID")

    # ユーザーID (UUID) - userテーブルのuser_idを参照する外部キー
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.user_id"), nullable=False, comment="ユーザーID (UUID)")

    # レポートID (UUID) - reportテーブルのreport_idを参照する外部キー
    report_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("report.report_id"), nullable=False, comment="レポートID (UUID)")

    # 閲覧日時 - レポートが閲覧された日時
    view_date: Mapped[datetime] = mapped_column(TIMESTAMP, comment="閲覧日時")

    # 作成日時
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime_now(), comment="作成日時")

    # 更新日時
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime_now(), onupdate=datetime_now(), comment="更新日時")

    # 削除日時
    deleted_at: Mapped[datetime | None] = mapped_column(TIMESTAMP, nullable=True, comment="削除日時")
