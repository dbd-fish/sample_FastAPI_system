from sqlalchemy import Column, String, TIMESTAMP, ForeignKey
from app.common.common import datetime_now
from app.database import Base
from sqlalchemy.dialects.postgresql import UUID

# UserGroupモデル: ユーザーグループ管理テーブル
class UserGroup(Base):
    __tablename__ = "user_group"
    
    # グループID (UUID) - プライマリキー
    group_id = Column(UUID(as_uuid=True), primary_key=True, comment="グループID (UUID)")
    
    # グループ名 - 一意でなければならない
    group_name = Column(String(50), unique=True, nullable=False, comment="グループ名")
    
    # 親グループID - user_groupテーブルのgroup_idを参照する外部キー
    parent_group_id = Column(UUID(as_uuid=True), ForeignKey("user_group.group_id"), nullable=True, comment="親グループID (UUID)")
    
    # 作成日時
    created_at = Column(TIMESTAMP, default=datetime_now(), comment="作成日時")
    
    # 更新日時
    updated_at = Column(TIMESTAMP,  default=datetime_now(), onupdate=datetime_now(), comment="更新日時")
    
    # 削除日時
    deleted_at = Column(TIMESTAMP, nullable=True, comment="削除日時")
