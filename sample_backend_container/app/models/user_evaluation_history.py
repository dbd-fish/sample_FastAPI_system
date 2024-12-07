import uuid
from datetime import datetime

from sqlalchemy import TIMESTAMP, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.common.common import datetime_now
from app.database import Base


# UserEvaluationHistoryモデル: ユーザー評価履歴テーブル
class UserEvaluationHistory(Base):
    __tablename__ = "user_evaluation_history"

    # 評価履歴ID - プライマリキー、自動インクリメント
    history_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="評価履歴ID")

    # 評価対象のユーザーID (UUID) - userテーブルのuser_idを参照する外部キー
    target_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.user_id"), nullable=False, comment="評価対象のユーザーID")

    # 評価者のユーザーID (UUID) - userテーブルのuser_idを参照する外部キー
    evaluator_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.user_id"), nullable=False, comment="評価者のユーザーID")

    # 評価スコア
    score: Mapped[int] = mapped_column(Integer, nullable=False, comment="評価スコア")

    # 作成日時
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime_now(), comment="作成日時")

    # 更新日時
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime_now(), onupdate=datetime_now(), comment="更新日時")

    # 削除日時
    deleted_at: Mapped[datetime | None] = mapped_column(TIMESTAMP, nullable=True, comment="削除日時")
