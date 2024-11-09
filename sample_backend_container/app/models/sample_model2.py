from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class SampleModel2(Base):
    __tablename__ = 'sample_table2'  # テーブル名を指定
    id = Column(Integer, primary_key=True, index=True)  # プライマリキー
    name = Column(String, nullable=False)  # 必須の名前カラム
    description = Column(String, nullable=True)  # オプションの説明カラム

    # 外部キーを使って、他のテーブルと関係を持たせる例
    related_id = Column(Integer, ForeignKey('sample_table.id'))  # 他のテーブルを参照
    related_item = relationship('SampleModel')  # 関連テーブルとのリレーションシップ
