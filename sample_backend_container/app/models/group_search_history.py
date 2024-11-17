
from sqlalchemy import Column, Integer, CHAR, String, TIMESTAMP, ForeignKey, func
from app.database import Base
from sqlalchemy.dialects.postgresql import UUID
# GroupSearchHistoryモデル: グループ検索履歴テーブル
class GroupSearchHistory(Base):
    __tablename__ = "group_search_history"

    # 検索ID - プライマリキー、自動インクリメント
    search_id = Column(Integer, primary_key=True, autoincrement=True, comment="検索ID")

    # ユーザーID (UUID) - 検索を行ったユーザー。userテーブルのuser_idを参照する外部キー
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.user_id"), nullable=False, comment="ユーザーID (UUID)")

    # 検索キーワード - ユーザーが入力した検索語句
    search_term = Column(String(100), comment="検索キーワード")

    # 検索日時 - 検索が行われた日時
    search_date = Column(TIMESTAMP, server_default=func.now(), comment="検索日時")

    # 作成日時
    created_at = Column(TIMESTAMP, server_default=func.now(), comment="作成日時")

    # 更新日時
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), comment="更新日時")

    # 削除日時
    deleted_at = Column(TIMESTAMP, nullable=True, comment="削除日時")
