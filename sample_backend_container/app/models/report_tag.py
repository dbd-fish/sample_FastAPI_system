from datetime import datetime

from sqlalchemy import TIMESTAMP, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.common.common import datetime_now
from app.database import Base


# ReportTagモデル: タグ管理テーブル
class ReportTag(Base):
    __tablename__ = "report_tag"

    # タグID - プライマリキー、自動インクリメント
    tag_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="タグID")

    # タグ名 - タグの名前、一意でなければならない
    tag_name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment="タグ名")

    # 作成日時
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime_now(), comment="作成日時")

    # 更新日時
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime_now(), onupdate=datetime_now(), comment="更新日時")

    # 削除日時
    deleted_at: Mapped[datetime | None] = mapped_column(TIMESTAMP, nullable=True, comment="削除日時")
