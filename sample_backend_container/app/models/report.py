
from sqlalchemy import Column, CHAR, String, Text, SmallInteger, TIMESTAMP, ForeignKey
from app.database import Base

# Reportモデル: レポート管理テーブル
class Report(Base):
    __tablename__ = "report"
    
    # レポートID (UUID) - プライマリキー
    report_id = Column(CHAR(36), primary_key=True, comment="レポートID (UUID)")
    
    # 作成者ユーザーID (UUID) - userテーブルのuser_idを参照する外部キー
    user_id = Column(CHAR(36), ForeignKey("user.user_id"), nullable=False, comment="作成者ユーザーID (UUID)")
    
    # タイトル - レポートのタイトル
    title = Column(String(100), nullable=False, comment="タイトル")
    
    # 内容 - レポートの本文
    content = Column(Text, comment="内容")
    
    # フォーマット - 1: md, 2: html
    format = Column(SmallInteger, default=1, nullable=False, comment="フォーマット (1: md, 2: html)")
    
    # 公開設定 - 1: public, 2: group, 3: private
    visibility = Column(SmallInteger, default=3, nullable=False, comment="公開設定 (1: public, 2: group, 3: private)")
    
    # 作成日時
    created_at = Column(TIMESTAMP, default="CURRENT_TIMESTAMP", comment="作成日時")
    
    # 更新日時
    updated_at = Column(TIMESTAMP, default="CURRENT_TIMESTAMP", onupdate="CURRENT_TIMESTAMP", comment="更新日時")
    
    # 削除日時
    deleted_at = Column(TIMESTAMP, nullable=True, comment="削除日時")
