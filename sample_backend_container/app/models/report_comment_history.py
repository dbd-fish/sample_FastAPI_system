
from sqlalchemy import Column, Integer, CHAR, Text, SmallInteger, TIMESTAMP, ForeignKey
from app.database import Base

# ReportCommentHistoryモデル: レポート補足履歴テーブル
class ReportCommentHistory(Base):
    __tablename__ = "report_comment_history"
    
    # レポート補足履歴ID - プライマリキー、自動インクリメント
    history_id = Column(Integer, primary_key=True, autoincrement=True, comment="レポート補足履歴ID")
    
    # レポート補足ID - report_supplementテーブルのreport_supplementを参照する外部キー
    report_supplement = Column(Integer, ForeignKey("report_supplement.report_supplement"), nullable=False, comment="レポート補足ID")
    
    # ユーザーID (UUID) - userテーブルのuser_idを参照する外部キー
    user_id = Column(CHAR(36), ForeignKey("user.user_id"), nullable=False, comment="ユーザーID (UUID)")
    
    # レポートID (UUID) - reportテーブルのreport_idを参照する外部キー
    report_id = Column(CHAR(36), ForeignKey("report.report_id"), nullable=False, comment="レポートID (UUID)")
    
    # コメント内容 - レポートに対するコメント内容
    content = Column(Text, comment="コメント内容")
    
    # アクション - 1: created, 2: updated, 3: deleted
    report_supplement_action = Column(SmallInteger, nullable=False, comment="アクション (1: created, 2: updated, 3: deleted)")
    
    # 作成日時
    created_at = Column(TIMESTAMP, default="CURRENT_TIMESTAMP", comment="作成日時")
    
    # 更新日時
    updated_at = Column(TIMESTAMP, default="CURRENT_TIMESTAMP", onupdate="CURRENT_TIMESTAMP", comment="更新日時")
    
    # 削除日時
    deleted_at = Column(TIMESTAMP, nullable=True, comment="削除日時")
