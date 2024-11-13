
from sqlalchemy import Column, Integer, CHAR, Text, TIMESTAMP, ForeignKey
from app.database import Base

# ReportSupplementモデル: レポート補足テーブル
class ReportSupplement(Base):
    __tablename__ = "report_supplement"
    
    # レポート補足ID - プライマリキー、自動インクリメント
    report_supplement = Column(Integer, primary_key=True, autoincrement=True, comment="レポート補足ID")
    
    # レポートID (UUID) - reportテーブルのreport_idを参照する外部キー
    report_id = Column(CHAR(36), ForeignKey("report.report_id"), nullable=False, comment="レポートID (UUID)")
    
    # ユーザーID (UUID) - userテーブルのuser_idを参照する外部キー
    user_id = Column(CHAR(36), ForeignKey("user.user_id"), nullable=False, comment="ユーザーID (UUID)")
    
    # レポート補足内容 - レポートに関する追加の説明やコメント
    content = Column(Text, comment="レポート補足内容")
    
    # レポート補足開始位置 - 補足内容の開始位置
    start_report = Column(Integer, comment="レポート補足開始位置")
    
    # レポート補足終了位置 - 補足内容の終了位置
    end_report = Column(Integer, comment="レポート補足終了位置")
    
    # レポート補足根拠 - 補足の参照URL
    supplement_url = Column(Text, comment="レポート補足根拠")
    
    # 作成日時
    created_at = Column(TIMESTAMP, default="CURRENT_TIMESTAMP", comment="作成日時")
    
    # 更新日時
    updated_at = Column(TIMESTAMP, default="CURRENT_TIMESTAMP", onupdate="CURRENT_TIMESTAMP", comment="更新日時")
    
    # 削除日時
    deleted_at = Column(TIMESTAMP, nullable=True, comment="削除日時")
