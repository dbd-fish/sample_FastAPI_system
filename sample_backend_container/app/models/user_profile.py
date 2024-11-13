from sqlalchemy import Column, Integer, CHAR, String, Text, TIMESTAMP, ForeignKey
from app.database import Base

# UserProfileモデル: ユーザープロフィールテーブル
class UserProfile(Base):
    __tablename__ = "user_profile"
    
    # プロフィールID - プライマリキー、自動インクリメント
    profile_id = Column(Integer, primary_key=True, autoincrement=True, comment="プロフィールID")
    
    # ユーザーID (UUID) - userテーブルのuser_idを参照する外部キー
    user_id = Column(CHAR(36), ForeignKey("user.user_id", ondelete="CASCADE"), nullable=False, comment="ユーザーID (UUID)")
    
    # 表示名 - プロフィール画面に表示される名前
    display_name = Column(String(100), comment="表示名")
    
    # プロフィール説明 - ユーザーが自身のプロフィールに追加できる自己紹介や説明文
    profile_text = Column(Text, comment="プロフィール説明")
    
    # プロフィール画像URL - プロフィール画像のURLを格納
    profile_image_url = Column(String(255), comment="プロフィール画像URL")
    
    # 作成日時
    created_at = Column(TIMESTAMP, default="CURRENT_TIMESTAMP", comment="作成日時")
    
    # 更新日時
    updated_at = Column(TIMESTAMP, default="CURRENT_TIMESTAMP", onupdate="CURRENT_TIMESTAMP", comment="更新日時")

    # 削除日時
    deleted_at = Column(TIMESTAMP, nullable=True, comment="削除日時")