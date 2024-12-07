import uuid
from datetime import datetime

from sqlalchemy import TIMESTAMP, ForeignKey, SmallInteger, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.common.common import datetime_now
from app.database import Base


# Reportモデル: レポート管理テーブル
class Report(Base):
    """Reportモデル: レポート管理テーブル
    """

    __tablename__ = "report"

    # フォーマットを定数として定義
    FORMAT_MD = 1     # Markdown形式
    FORMAT_HTML = 2   # HTML形式

    # 公開設定を定数として定義
    VISIBILITY_PUBLIC = 1   # 公開
    VISIBILITY_GROUP = 2    # グループ限定
    VISIBILITY_PRIVATE = 3  # 非公開

    # レポートID (UUID) - プライマリキー
    report_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, comment="レポートID (UUID)")

    # 作成者ユーザーID (UUID) - userテーブルのuser_idを参照する外部キー
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.user_id"), nullable=False, comment="作成者ユーザーID (UUID)")

    # タイトル - レポートのタイトル
    title: Mapped[str] = mapped_column(String(100), nullable=False, comment="タイトル")

    # 内容 - レポートの本文
    content: Mapped[str | None] = mapped_column(Text, comment="内容")

    # フォーマット - 1: md, 2: html
    format: Mapped[int] = mapped_column(SmallInteger, default=FORMAT_MD, nullable=False, comment="フォーマット (1: md, 2: html)")

    # 公開設定 - 1: public, 2: group, 3: private
    visibility: Mapped[int] = mapped_column(SmallInteger, default=VISIBILITY_PRIVATE, nullable=False, comment="公開設定 (1: public, 2: group, 3: private)")

    # 作成日時
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime_now(), comment="作成日時")

    # 更新日時
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime_now(), onupdate=datetime_now(), comment="更新日時")

    # 削除日時
    deleted_at: Mapped[datetime | None] = mapped_column(TIMESTAMP, nullable=True, comment="削除日時")
