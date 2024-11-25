from sqlalchemy import Column, Integer, Text, SmallInteger, TIMESTAMP, ForeignKey
from app.common.common import datetime_now
from app.database import Base
from sqlalchemy.dialects.postgresql import UUID


class ReportCommentHistory(Base):
    """
    ReportCommentHistoryモデル: レポート補足履歴テーブル
    """
    __tablename__ = "report_comment_history"
    
    # アクションを定数として定義
    ACTION_CREATED = 1  # 作成
    ACTION_UPDATED = 2  # 更新
    ACTION_DELETED = 3  # 削除

    # レポート補足履歴ID - プライマリキー、自動インクリメント
    history_id = Column(Integer, primary_key=True, autoincrement=True, comment="レポート補足履歴ID")
    
    # レポート補足ID - report_supplementテーブルのreport_supplementを参照する外部キー
    report_supplement = Column(Integer, ForeignKey("report_supplement.report_supplement"), nullable=False, comment="レポート補足ID")
    
    # ユーザーID (UUID) - userテーブルのuser_idを参照する外部キー
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.user_id"), nullable=False, comment="ユーザーID (UUID)")
    
    # レポートID (UUID) - reportテーブルのreport_idを参照する外部キー
    report_id = Column(UUID(as_uuid=True), ForeignKey("report.report_id"), nullable=False, comment="レポートID (UUID)")
    
    # コメント内容 - レポートに対するコメント内容
    content = Column(Text, comment="コメント内容")
    
    # アクション - 1: created, 2: updated, 3: deleted
    # 1つのレポート補足に対する操作履歴
    report_supplement_action = Column(SmallInteger, nullable=False, comment="アクション (1: created, 2: updated, 3: deleted)")
    
    # 作成日時
    created_at = Column(TIMESTAMP, default=datetime_now(), comment="作成日時")
    
    # 更新日時
    updated_at = Column(TIMESTAMP,  default=datetime_now(), onupdate=datetime_now(), comment="更新日時")
    
    # 削除日時
    deleted_at = Column(TIMESTAMP, nullable=True, comment="削除日時")
