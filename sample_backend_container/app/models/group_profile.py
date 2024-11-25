
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from app.common.common import datetime_now
from app.database import Base
from sqlalchemy.dialects.postgresql import UUID
# GroupProfileモデル: グループプロフィールテーブル
class GroupProfile(Base):
    __tablename__ = "group_profile"
    
    # プロフィールID - プライマリキー、自動インクリメント
    profile_id = Column(Integer, primary_key=True, autoincrement=True, comment="プロフィールID")
    
    # グループID (UUID) - user_groupテーブルのgroup_idを参照する外部キー
    group_id = Column(UUID(as_uuid=True), ForeignKey("user_group.group_id", ondelete="CASCADE"), nullable=False, comment="グループID (UUID)")
    
    # グループ表示名
    display_name = Column(String(100), comment="グループ表示名")
    
    # グループプロフィール説明
    profile_text = Column(Text, comment="グループプロフィール説明")
    
    # グループプロフィール画像URL
    profile_image_url = Column(String(255), comment="グループプロフィール画像URL")
    
    # 作成日時
    created_at = Column(TIMESTAMP, default=datetime_now(), comment="作成日時")
    
    # 更新日時
    updated_at = Column(TIMESTAMP,  default=datetime_now(), onupdate=datetime_now(), comment="更新日時")

    # 削除日時
    deleted_at = Column(TIMESTAMP, nullable=True, comment="削除日時")