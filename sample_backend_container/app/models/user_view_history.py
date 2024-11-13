
from sqlalchemy import Column, Integer, CHAR, TIMESTAMP, ForeignKey
from app.database import Base

# UserViewHistoryモデル: ユーザー閲覧履歴テーブル
class UserViewHistory(Base):
    __tablename__ = "user_view_history"

    # 履歴ID - プライマリキー、自動インクリメント
    history_id = Column(Integer, primary_key=True, autoincrement=True, comment="履歴ID")

    # 閲覧者ID (UUID) - userテーブルのuser_idを参照する外部キー
    viewer_id = Column(CHAR(36), ForeignKey("user.user_id"), nullable=False, comment="閲覧者ID (UUID)")

    # 閲覧対象ユーザーID (UUID) - userテーブルのuser_idを参照する外部キー
    viewed_user_id = Column(CHAR(36), ForeignKey("user.user_id"), nullable=False, comment="閲覧対象ユーザーID (UUID)")

    # 作成日時
    created_at = Column(TIMESTAMP, default="CURRENT_TIMESTAMP", comment="作成日時")

    # 閲覧日時 - ユーザーが閲覧された日時
    view_date = Column(TIMESTAMP, default="CURRENT_TIMESTAMP", comment="閲覧日時")

    # 更新日時 - レコードが最後に更新された日時
    updated_at = Column(TIMESTAMP, default="CURRENT_TIMESTAMP", onupdate="CURRENT_TIMESTAMP", comment="更新日時")

    # 削除日時
    deleted_at = Column(TIMESTAMP, nullable=True, comment="削除日時")
