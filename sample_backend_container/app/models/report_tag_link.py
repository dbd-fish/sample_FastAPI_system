import uuid
from datetime import datetime

from sqlalchemy import TIMESTAMP, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.common.common import datetime_now
from app.database import Base


# ReportTagLinkモデル: レポートとタグの関連テーブル
class ReportTagLink(Base):
    __tablename__ = "report_tag_link"

    # レポートID (UUID) - reportテーブルのreport_idを参照する外部キー
    report_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("report.report_id"), primary_key=True, nullable=False, comment="レポートID (UUID)")

    # タグID - report_tagテーブルのtag_idを参照する外部キー
    tag_id: Mapped[int] = mapped_column(Integer, ForeignKey("report_tag.tag_id"), primary_key=True, nullable=False, comment="タグID")

    # 作成日時
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime_now(), comment="作成日時")

    # 更新日時
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime_now(), onupdate=datetime_now(), comment="更新日時")

    # 削除日時
    deleted_at: Mapped[datetime | None] = mapped_column(TIMESTAMP, nullable=True, comment="削除日時")
