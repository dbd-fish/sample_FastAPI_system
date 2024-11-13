
from sqlalchemy import Column, CHAR, TIMESTAMP, ForeignKey
from app.database import Base

# UserGroupMembershipモデル: ユーザーとグループの関連テーブル
class UserGroupMembership(Base):
    __tablename__ = "user_group_membership"
    
    # ユーザーID (UUID) - userテーブルのuser_idを参照する外部キー
    user_id = Column(CHAR(36), ForeignKey("user.user_id"), primary_key=True, nullable=False, comment="ユーザーID (UUID)")
    
    # グループID (UUID) - user_groupテーブルのgroup_idを参照する外部キー
    group_id = Column(CHAR(36), ForeignKey("user_group.group_id"), primary_key=True, nullable=False, comment="グループID (UUID)")
    
    # 作成日時
    created_at = Column(TIMESTAMP, default="CURRENT_TIMESTAMP", comment="作成日時")
    
    # 更新日時
    updated_at = Column(TIMESTAMP, default="CURRENT_TIMESTAMP", onupdate="CURRENT_TIMESTAMP", comment="更新日時")
    
    # 削除日時
    deleted_at = Column(TIMESTAMP, nullable=True, comment="削除日時")
