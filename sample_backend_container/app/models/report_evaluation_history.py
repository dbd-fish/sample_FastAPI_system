import uuid
from datetime import datetime

from sqlalchemy import TIMESTAMP, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.common.common import datetime_now
from app.database import Base


# ReportEvaluationHistoryモデル: レポート評価履歴テーブル
class ReportEvaluationHistory(Base):
    __tablename__ = "report_evaluation_history"

    # 評価履歴ID - プライマリキー、自動インクリメント
    evaluation_history_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="評価履歴ID")

    # レポートID (UUID) - reportテーブルのreport_idを参照する外部キー
    report_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("report.report_id"), nullable=False, comment="レポートID (UUID)")

    # ユーザーID (UUID) - userテーブルのuser_idを参照する外部キー
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.user_id"), nullable=False, comment="ユーザーID (UUID)")

    # 評価スコア - 評価点数（整数値）
    score: Mapped[int] = mapped_column(Integer, nullable=False, comment="評価スコア")

    # 作成日時
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime_now(), comment="作成日時")

    # 更新日時
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime_now(), onupdate=datetime_now(), comment="更新日時")

    # 削除日時
    deleted_at: Mapped[datetime | None] = mapped_column(TIMESTAMP, nullable=True, comment="削除日時")
