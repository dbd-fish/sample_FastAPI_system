from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from app.common.common import datetime_now
from app.database import Base
from sqlalchemy.dialects.postgresql import UUID

# UserProfileモデル: ユーザープロフィールテーブル
class UserProfile(Base):
    __tablename__ = "user_profile"
    
    # プロフィールID - プライマリキー、自動インクリメント
    profile_id = Column(Integer, primary_key=True, autoincrement=True, comment="プロフィールID")
    
    # ユーザーID (UUID) - userテーブルのuser_idを参照する外部キー
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.user_id", ondelete="CASCADE"), nullable=False, comment="ユーザーID (UUID)")
    
    # 表示名 - プロフィール画面に表示される名前
    display_name = Column(String(100), comment="表示名")
    
    # プロフィール説明 - ユーザーが自身のプロフィールに追加できる自己紹介や説明文
    profile_text = Column(Text, comment="プロフィール説明")
    
    # プロフィール画像URL - プロフィール画像のURLを格納
    profile_image_url = Column(String(255), comment="プロフィール画像URL")
    
    # 作成日時
    created_at = Column(TIMESTAMP, default=datetime_now(), comment="作成日時")
    
    # 更新日時
    updated_at = Column(TIMESTAMP,  default=datetime_now(), onupdate=datetime_now(), comment="更新日時")

    # 削除日時
    deleted_at = Column(TIMESTAMP, nullable=True, comment="削除日時")