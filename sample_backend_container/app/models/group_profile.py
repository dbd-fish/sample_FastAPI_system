import uuid
from datetime import datetime

from sqlalchemy import TIMESTAMP, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.common.common import datetime_now
from app.database import Base


# GroupProfileモデル: グループプロフィールテーブル
class GroupProfile(Base):
    __tablename__ = "group_profile"

    # プロフィールID - プライマリキー、自動インクリメント
    profile_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="プロフィールID")

    # グループID (UUID) - user_groupテーブルのgroup_idを参照する外部キー
    group_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user_group.group_id", ondelete="CASCADE"), nullable=False, comment="グループID (UUID)")

    # グループ表示名
    display_name: Mapped[str | None] = mapped_column(String(100), comment="グループ表示名")

    # グループプロフィール説明
    profile_text: Mapped[str | None] = mapped_column(Text, comment="グループプロフィール説明")

    # グループプロフィール画像URL
    profile_image_url: Mapped[str | None] = mapped_column(String(255), comment="グループプロフィール画像URL")

    # 作成日時
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime_now(), comment="作成日時")

    # 更新日時
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime_now(), onupdate=datetime_now(), comment="更新日時")

    # 削除日時
    deleted_at: Mapped[datetime | None] = mapped_column(TIMESTAMP, nullable=True, comment="削除日時")
