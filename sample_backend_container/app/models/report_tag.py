from sqlalchemy import Column, Integer, String, TIMESTAMP
from app.common.common import datetime_now
from app.database import Base
from datetime import datetime
from zoneinfo import ZoneInfo

# ReportTagモデル: タグ管理テーブル
class ReportTag(Base):
    __tablename__ = "report_tag"
    
    # タグID - プライマリキー、自動インクリメント
    tag_id = Column(Integer, primary_key=True, autoincrement=True, comment="タグID")
    
    # タグ名 - タグの名前、一意でなければならない
    tag_name = Column(String(50), unique=True, nullable=False, comment="タグ名")
    
    # 作成日時
    created_at = Column(TIMESTAMP, default=datetime_now(), comment="作成日時")
    
    # 更新日時
    updated_at = Column(TIMESTAMP,  default=datetime_now(), onupdate=datetime_now(), comment="更新日時")
    
    # 削除日時
    deleted_at = Column(TIMESTAMP, nullable=True, comment="削除日時")

