import uuid
from datetime import datetime

from sqlalchemy import TIMESTAMP, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.common.common import datetime_now
from app.database import Base


# GroupSearchHistoryモデル: グループ検索履歴テーブル
class GroupSearchHistory(Base):
    __tablename__ = "group_search_history"

    # 検索ID - プライマリキー、自動インクリメント
    search_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="検索ID")

    # ユーザーID (UUID) - 検索を行ったユーザー。userテーブルのuser_idを参照する外部キー
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.user_id"), nullable=False, comment="ユーザーID (UUID)")

    # 検索キーワード - ユーザーが入力した検索語句
    search_term: Mapped[str | None] = mapped_column(String(100), comment="検索キーワード")

    # 検索日時 - 検索が行われた日時
    search_date: Mapped[datetime] = mapped_column(TIMESTAMP, comment="検索日時")

    # 作成日時
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime_now(), comment="作成日時")

    # 更新日時
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime_now(), onupdate=datetime_now(), comment="更新日時")

    # 削除日時
    deleted_at: Mapped[datetime | None] = mapped_column(TIMESTAMP, nullable=True, comment="削除日時")
