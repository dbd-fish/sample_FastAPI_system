import uuid
from datetime import datetime

from sqlalchemy import TIMESTAMP, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.common.common import datetime_now
from app.database import Base


# ReportSupplementモデル: レポート補足情報テーブル
class ReportSupplement(Base):
    __tablename__ = "report_supplement"

    # 補足ID - プライマリキー、自動インクリメント
    supplement_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="補足ID")

    # レポートID (UUID) - reportテーブルのreport_idを参照する外部キー
    report_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("report.report_id"), nullable=False, comment="レポートID (UUID)")

    # ユーザーID (UUID) - userテーブルのuser_idを参照する外部キー
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.user_id"), nullable=False, comment="ユーザーID (UUID)")

    # 補足内容 - レポートに関連する追加の説明や情報
    content: Mapped[str | None] = mapped_column(Text, comment="補足内容")

    # 作成日時
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime_now(), comment="作成日時")

    # 更新日時
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime_now(), onupdate=datetime_now(), comment="更新日時")

    # 削除日時
    deleted_at: Mapped[datetime | None] = mapped_column(TIMESTAMP, nullable=True, comment="削除日時")
