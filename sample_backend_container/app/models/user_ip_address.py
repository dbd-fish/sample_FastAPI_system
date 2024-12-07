import uuid
from datetime import datetime

from sqlalchemy import TIMESTAMP, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.common.common import datetime_now
from app.database import Base


# UserIPAddressモデル: ユーザーのIPアドレス管理テーブル
class UserIPAddress(Base):
    __tablename__ = "user_ip_address"

    # IP ID - プライマリキー、自動インクリメント
    ip_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="IP ID")

    # ユーザーID (UUID) - userテーブルのuser_idを参照する外部キー、ユーザーとIPアドレスを関連付ける
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.user_id", ondelete="CASCADE"), nullable=False, comment="ユーザーID (UUID)")

    # IPアドレス - ユーザーの接続元IPアドレスを記録
    ip_address: Mapped[str] = mapped_column(String(45), nullable=False, comment="IPアドレス")

    # 作成日時
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime_now(), comment="作成日時")

    # 更新日時
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime_now(), onupdate=datetime_now(), comment="更新日時")

    # 削除日時
    deleted_at: Mapped[datetime | None] = mapped_column(TIMESTAMP, nullable=True, comment="削除日時")
