from sqlalchemy import Column, String, SmallInteger, TIMESTAMP, Date
from app.common.common import datetime_now
from app.database import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID


class User(Base):
    """
    Userモデル: ユーザー管理テーブル
    """
    __tablename__ = "user"

    # ユーザー権限を定数として定義
    ROLE_GUEST = 1      # ゲスト
    ROLE_FREE = 2       # 無料会員
    ROLE_REGULAR = 3    # 一般会員
    ROLE_ADMIN = 4      # 管理者
    ROLE_OWNER = 5      # オーナー

    # ユーザー状態を定数として定義
    STATUS_ACTIVE = 1   # アクティブ
    STATUS_SUSPENDED = 2 # 停止中

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

    # ユーザー権限
    user_role = Column(SmallInteger, nullable=False, comment="ユーザー権限 (1: guest, 2: free, 3: regular, 4: admin, 5: owner)")

    # アカウント状態
    user_status = Column(SmallInteger, nullable=False, comment="アカウント状態 (1: active, 2: suspended)")

    # 作成日時
    created_at = Column(TIMESTAMP, default=datetime_now(), comment="作成日時")

    # 更新日時 - 更新時に自動で変更
    updated_at = Column(TIMESTAMP, default=datetime_now(), onupdate=datetime_now(), comment="更新日時")

    # 削除日時
    deleted_at = Column(TIMESTAMP, nullable=True, comment="削除日時")
