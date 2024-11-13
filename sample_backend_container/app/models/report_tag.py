from sqlalchemy import Column, Integer, String, TIMESTAMP
from app.database import Base

# ReportTagモデル: タグ管理テーブル
class ReportTag(Base):
    __tablename__ = "report_tag"
    
    # タグID - プライマリキー、自動インクリメント
    tag_id = Column(Integer, primary_key=True, autoincrement=True, comment="タグID")
    
    # タグ名 - タグの名前、一意でなければならない
    tag_name = Column(String(50), unique=True, nullable=False, comment="タグ名")
    
    # 作成日時
    created_at = Column(TIMESTAMP, default="CURRENT_TIMESTAMP", comment="作成日時")
    
    # 更新日時
    updated_at = Column(TIMESTAMP, default="CURRENT_TIMESTAMP", onupdate="CURRENT_TIMESTAMP", comment="更新日時")
    
    # 削除日時
    deleted_at = Column(TIMESTAMP, nullable=True, comment="削除日時")

