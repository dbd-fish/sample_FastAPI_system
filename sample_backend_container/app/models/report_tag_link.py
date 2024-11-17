
from sqlalchemy import Column, CHAR, Integer, TIMESTAMP, ForeignKey, func
from app.database import Base
from sqlalchemy.dialects.postgresql import UUID

# ReportTagLinkモデル: レポートとタグの関連テーブル
class ReportTagLink(Base):
    __tablename__ = "report_tag_link"
    
    # レポートID (UUID) - reportテーブルのreport_idを参照する外部キー
    report_id = Column(UUID(as_uuid=True), ForeignKey("report.report_id"), primary_key=True, nullable=False, comment="レポートID (UUID)")
    
    # タグID - report_tagテーブルのtag_idを参照する外部キー
    tag_id = Column(Integer, ForeignKey("report_tag.tag_id"), primary_key=True, nullable=False, comment="タグID")
    
    # 作成日時
    created_at = Column(TIMESTAMP, server_default=func.now(), comment="作成日時")
    
    # 更新日時
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), comment="更新日時")
    
    # 削除日時
    deleted_at = Column(TIMESTAMP, nullable=True, comment="削除日時")
