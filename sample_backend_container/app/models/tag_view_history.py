from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID

from app.common.common import datetime_now
from app.database import Base


# TagViewHistoryモデル: タグ閲覧履歴テーブル
class TagViewHistory(Base):
    __tablename__ = "tag_view_history"

    # 履歴ID - プライマリキー、自動インクリメント
    history_id = Column(Integer, primary_key=True, autoincrement=True, comment="履歴ID")

    # ユーザーID (UUID) - userテーブルのuser_idを参照する外部キー
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.user_id"), nullable=False, comment="ユーザーID (UUID)")

    # タグID - report_tagテーブルのtag_idを参照する外部キー
    tag_id = Column(Integer, ForeignKey("report_tag.tag_id"), nullable=False, comment="タグID")

    # 閲覧日時 - タグが閲覧された日時
    view_date = Column(TIMESTAMP,  comment="閲覧日時")

    # 作成日時
    created_at = Column(TIMESTAMP, default=datetime_now(), comment="作成日時")

    # 更新日時
    updated_at = Column(TIMESTAMP,  default=datetime_now(), onupdate=datetime_now(), comment="更新日時")

    # 削除日時
    deleted_at = Column(TIMESTAMP, nullable=True, comment="削除日時")
