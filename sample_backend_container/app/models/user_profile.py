import uuid
from datetime import datetime

from sqlalchemy import TIMESTAMP, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.common.common import datetime_now
from app.database import Base


# UserProfileモデル: ユーザープロフィールテーブル
class UserProfile(Base):
    __tablename__ = "user_profile"

    # プロフィールID - プライマリキー、自動インクリメント
    profile_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="プロフィールID")

    # ユーザーID (UUID) - userテーブルのuser_idを参照する外部キー
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.user_id", ondelete="CASCADE"), nullable=False, comment="ユーザーID (UUID)")

    # 表示名 - プロフィール画面に表示される名前
    display_name: Mapped[str | None] = mapped_column(String(100), comment="表示名")

    # プロフィール説明 - ユーザーが自身のプロフィールに追加できる自己紹介や説明文
    profile_text: Mapped[str | None] = mapped_column(Text, comment="プロフィール説明")

    # プロフィール画像URL - プロフィール画像のURLを格納
    profile_image_url: Mapped[str | None] = mapped_column(String(255), comment="プロフィール画像URL")

    # 作成日時
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime_now(), comment="作成日時")

    # 更新日時
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime_now(), onupdate=datetime_now(), comment="更新日時")

    # 削除日時
    deleted_at: Mapped[datetime | None] = mapped_column(TIMESTAMP, nullable=True, comment="削除日時")
