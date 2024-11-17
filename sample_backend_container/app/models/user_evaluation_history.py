
from sqlalchemy import Column, Integer, CHAR, Text, TIMESTAMP, ForeignKey, func
from app.database import Base
from sqlalchemy.dialects.postgresql import UUID

# UserEvaluationHistoryモデル: ユーザー評価履歴テーブル
class UserEvaluationHistory(Base):
    __tablename__ = "user_evaluation_history"
    
    # 評価履歴ID - プライマリキー、自動インクリメント
    history_id = Column(Integer, primary_key=True, autoincrement=True, comment="評価履歴ID")
    
    # 評価ID
    eval_id = Column(Integer, nullable=False, comment="評価ID")
    
    # 評価を行ったユーザーID (UUID) - userテーブルのuser_idを参照する外部キー
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.user_id"), nullable=False, comment="評価を行ったユーザーID (UUID)")
    
    # 評価されたユーザーID (UUID) - userテーブルのuser_idを参照する外部キー
    target_user_id = Column(UUID(as_uuid=True), ForeignKey("user.user_id"), nullable=False, comment="評価されたユーザーID (UUID)")
    
    # 評価スコア - ユーザーへの評価スコア
    score = Column(Integer, comment="評価スコア")
    
    # 評価コメント - 評価に関するコメント
    comment = Column(Text, comment="評価コメント")
    
    # 作成日時
    created_at = Column(TIMESTAMP, server_default=func.now(), comment="作成日時")
    
    # 更新日時
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), comment="更新日時")

    # 削除日時
    deleted_at = Column(TIMESTAMP, nullable=True, comment="削除日時")