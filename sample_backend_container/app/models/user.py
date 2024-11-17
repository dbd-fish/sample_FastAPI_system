from sqlalchemy import Column, CHAR, String, SmallInteger, TIMESTAMP, Date, func
from app.database import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID

# Userモデル: ユーザー管理テーブル
class User(Base):
    __tablename__ = "user"
    
    # ユーザーID (UUID) - プライマリキー
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, comment="ユーザーID (UUID)")
    
    # ユーザー名 - 50文字以内
    username = Column(String(50), nullable=False, comment="ユーザー名")
    
    # メールアドレス - 一意でなければならない
    email = Column(String(100), unique=True, nullable=False, comment="メールアドレス")
    
    # パスワードハッシュ
    password_hash = Column(String(255), nullable=False, comment="パスワード（ハッシュ）")
    
    # 連絡先電話番号
    contact_number = Column(String(15), comment="連絡先電話番号")
    
    # 生年月日
    date_of_birth = Column(Date, comment="生年月日")
    
    # ユーザー権限 - 1: guest, 2: free, 3: regular, 4: admin, 5: owner
    # このフィールドはユーザーの権限レベルを表す整数で、次のように区分されています:
    # 1はゲスト（guest）、2は無料会員（free）、3は一般会員（regular）、4は管理者（admin）、5はオーナー（owner）
    user_role = Column(SmallInteger, nullable=False, comment="ユーザー権限 (1: guest, 2: free, 3: regular, 4: admin, 5: owner)")

    # アカウント状態 - 1: active, 2: suspended
    user_status = Column(SmallInteger, nullable=False, comment="アカウント状態 (1: active, 2: suspended)")
    
    # 作成日時
    created_at = Column(TIMESTAMP, server_default=func.now(), comment="作成日時")
    
    # 更新日時 - 更新時に自動で変更
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), comment="更新日時")
    
    # 削除日時
    deleted_at = Column(TIMESTAMP, nullable=True, comment="削除日時")

