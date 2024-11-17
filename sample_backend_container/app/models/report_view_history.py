
from sqlalchemy import Column, Integer, CHAR, TIMESTAMP, ForeignKey, func
from app.database import Base
from sqlalchemy.dialects.postgresql import UUID

# ReportViewHistoryモデル: レポート閲覧履歴テーブル
class ReportViewHistory(Base):
    __tablename__ = "report_view_history"
    
    # 履歴ID - プライマリキー、自動インクリメント
    history_id = Column(Integer, primary_key=True, autoincrement=True, comment="履歴ID")
    
    # ユーザーID (UUID) - userテーブルのuser_idを参照する外部キー
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.user_id"), nullable=False, comment="ユーザーID (UUID)")
    
    # レポートID (UUID) - reportテーブルのreport_idを参照する外部キー
    report_id = Column(UUID(as_uuid=True), ForeignKey("report.report_id"), nullable=False, comment="レポートID (UUID)")
    
    # 閲覧日時 - レポートが閲覧された日時
    view_date = Column(TIMESTAMP, server_default=func.now(), comment="閲覧日時")

    # 作成日時
    created_at = Column(TIMESTAMP, server_default=func.now(), comment="作成日時")
   
    # 更新日時
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), comment="更新日時")
    
    # 削除日時
    deleted_at = Column(TIMESTAMP, nullable=True, comment="削除日時")
