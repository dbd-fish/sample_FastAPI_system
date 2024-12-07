from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, TIMESTAMP, ForeignKey, Integer
from app.common.common import datetime_now
from app.database import Base
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

# UserGroupモデル: ユーザーグループテーブル
class UserGroup(Base):
    __tablename__ = "user_group"

    # グループID (UUID) - プライマリキー
    group_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, comment="グループID (UUID)")

    # グループ名
    group_name: Mapped[str] = mapped_column(String(50), nullable=False, comment="グループ名")

    # 作成日時
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime_now(), comment="作成日時")

    # 更新日時
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime_now(), onupdate=datetime_now(), comment="更新日時")

    # 削除日時
    deleted_at: Mapped[datetime | None] = mapped_column(TIMESTAMP, nullable=True, comment="削除日時")
