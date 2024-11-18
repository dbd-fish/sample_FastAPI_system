
from sqlalchemy import Column, Integer, CHAR, Text, TIMESTAMP, ForeignKey
from app.common.common import datetime_now
from app.database import Base
from datetime import datetime
from zoneinfo import ZoneInfo
from sqlalchemy.dialects.postgresql import UUID

# GroupEvaluationモデル: グループ評価テーブル
class GroupEvaluation(Base):
    __tablename__ = "group_evaluation"
    
    # 評価ID - プライマリキー、自動インクリメント
    eval_id = Column(Integer, primary_key=True, autoincrement=True, comment="評価ID")
    
    # 評価者ID (UUID) - userテーブルのuser_idを参照する外部キー
    evaluator_id = Column(UUID(as_uuid=True), ForeignKey("user.user_id"), nullable=False, comment="評価者ID (UUID)")
    
    # グループID (UUID) - user_groupテーブルのgroup_idを参照する外部キー
    group_id = Column(UUID(as_uuid=True), ForeignKey("user_group.group_id"), nullable=False, comment="グループID (UUID)")
    
    # 評価スコア - グループに対する評価スコア（0から100の間で制約）
    score = Column(Integer, nullable=False, comment="評価スコア")
    
    # 評価コメント - 評価に関するコメント
    comment = Column(Text, comment="評価コメント")
    
    # 作成日時
    created_at = Column(TIMESTAMP, default=datetime_now(), comment="作成日時")
    
    # 更新日時
    updated_at = Column(TIMESTAMP,  default=datetime_now(), onupdate=datetime_now(), comment="更新日時")
    
    # 削除日時
    deleted_at = Column(TIMESTAMP, nullable=True, comment="削除日時")
