from sqlalchemy import Column, CHAR, String, Text, SmallInteger, TIMESTAMP, ForeignKey
from app.common.common import datetime_now
from app.database import Base
from datetime import datetime
from zoneinfo import ZoneInfo
import uuid
from sqlalchemy.dialects.postgresql import UUID


# Reportモデル: レポート管理テーブル
class Report(Base):
    """
    Reportモデル: レポート管理テーブル
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
    report_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, comment="レポートID (UUID)")

    # 作成者ユーザーID (UUID) - userテーブルのuser_idを参照する外部キー
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.user_id"), nullable=False, comment="作成者ユーザーID (UUID)")

    # タイトル - レポートのタイトル
    title = Column(String(100), nullable=False, comment="タイトル")

    # 内容 - レポートの本文
    content = Column(Text, comment="内容")

    # フォーマット - 1: md, 2: html
    format = Column(SmallInteger, default=FORMAT_MD, nullable=False, comment="フォーマット (1: md, 2: html)")

    # 公開設定 - 1: public, 2: group, 3: private
    visibility = Column(SmallInteger, default=VISIBILITY_PRIVATE, nullable=False, comment="公開設定 (1: public, 2: group, 3: private)")

    # 作成日時
    created_at = Column(TIMESTAMP, default=datetime_now(), comment="作成日時")

    # 更新日時
    updated_at = Column(TIMESTAMP,  default=datetime_now(), onupdate=datetime_now(), comment="更新日時")

    # 削除日時
    deleted_at = Column(TIMESTAMP, nullable=True, comment="削除日時")
