from sqlalchemy import Column, Integer, CHAR, String, TIMESTAMP, ForeignKey
from app.common.common import datetime_now
from app.database import Base
from datetime import datetime
from zoneinfo import ZoneInfo
from sqlalchemy.dialects.postgresql import UUID

# UserIPAddressモデル: ユーザーのIPアドレス管理テーブル
class UserIPAddress(Base):
    __tablename__ = "user_ip_address"
    
    # IP ID - プライマリキー、自動インクリメント
    ip_id = Column(Integer, primary_key=True, autoincrement=True, comment="IP ID")
    
    # ユーザーID (UUID) - userテーブルのuser_idを参照する外部キー、ユーザーとIPアドレスを関連付ける
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.user_id", ondelete="CASCADE"), nullable=False, comment="ユーザーID (UUID)")
    
    # IPアドレス - ユーザーの接続元IPアドレスを記録
    ip_address = Column(String(45), nullable=False, comment="IPアドレス")
    
    # 作成日時
    created_at = Column(TIMESTAMP, default=datetime_now(), comment="作成日時")
    
    # 更新日時
    updated_at = Column(TIMESTAMP,  default=datetime_now(), onupdate=datetime_now(), comment="更新日時")
    
    # 削除日時
    deleted_at = Column(TIMESTAMP, nullable=True, comment="削除日時")

