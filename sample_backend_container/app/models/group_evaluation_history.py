from sqlalchemy import Column, Integer, CHAR, Text, TIMESTAMP, ForeignKey, func
from app.database import Base
from sqlalchemy.dialects.postgresql import UUID

# GroupEvaluationHistoryモデル: グループ評価履歴テーブル
class GroupEvaluationHistory(Base):
    __tablename__ = "group_evaluation_history"
    
    # 評価履歴ID - プライマリキー、自動インクリメント
    history_id = Column(Integer, primary_key=True, autoincrement=True, comment="評価履歴ID")
    
    # 評価ID
    eval_id = Column(Integer, nullable=False, comment="評価ID")
    
    # 評価者ユーザーID (UUID) - userテーブルのuser_idを参照する外部キー
    evaluator_id = Column(UUID(as_uuid=True), ForeignKey("user.user_id"), nullable=False, comment="評価者ユーザーID (UUID)")
    
    # グループID (UUID) - user_groupテーブルのgroup_idを参照する外部キー
    group_id = Column(UUID(as_uuid=True), ForeignKey("user_group.group_id"), nullable=False, comment="グループID (UUID)")
    
    # 評価スコア - グループの評価スコア
    score = Column(Integer, comment="評価スコア")
    
    # 評価コメント - グループの評価に関するコメント
    comment = Column(Text, comment="評価コメント")
    
    # 作成日時
    created_at = Column(TIMESTAMP, server_default=func.now(), comment="作成日時")
    
    # 更新日時
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), comment="更新日時")

    # 削除日時
    deleted_at = Column(TIMESTAMP, nullable=True, comment="削除日時")