import uuid
from datetime import datetime

from sqlalchemy import TIMESTAMP, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.common.common import datetime_now
from app.database import Base


# GroupEvaluationHistoryモデル: グループ評価履歴テーブル
class GroupEvaluationHistory(Base):
    __tablename__ = "group_evaluation_history"

    # 評価履歴ID - プライマリキー、自動インクリメント
    history_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="評価履歴ID")

    # 評価ID
    eval_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="評価ID")

    # 評価者ユーザーID (UUID) - userテーブルのuser_idを参照する外部キー
    evaluator_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.user_id"), nullable=False, comment="評価者ユーザーID (UUID)")

    # グループID (UUID) - user_groupテーブルのgroup_idを参照する外部キー
    group_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user_group.group_id"), nullable=False, comment="グループID (UUID)")

    # 評価スコア - グループの評価スコア
    score: Mapped[int | None] = mapped_column(Integer, comment="評価スコア")

    # 評価コメント - グループの評価に関するコメント
    comment: Mapped[str | None] = mapped_column(Text, comment="評価コメント")

    # 作成日時
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime_now(), comment="作成日時")

    # 更新日時
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime_now(), onupdate=datetime_now(), comment="更新日時")

    # 削除日時
    deleted_at: Mapped[datetime | None] = mapped_column(TIMESTAMP, nullable=True, comment="削除日時")
