from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from sqlalchemy.exc import SQLAlchemyError
from uuid import UUID


class UserRepository:
    """ユーザー関連のデータベース操作を担当するリポジトリクラス。"""

    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
        """
        メールアドレスに基づいてユーザーを取得します。

        Args:
            db (AsyncSession): 非同期データベースセッション。
            email (str): 検索対象のメールアドレス。

        Returns:
            User | None: 該当するユーザーが存在すれば返却、それ以外はNone。
        """
        query = select(User).where(User.email == email)
        result = await db.execute(query)
        return result.scalars().first()

    @staticmethod
    async def create_user(db: AsyncSession, user: User) -> User:
        """
        新しいユーザーをデータベースに登録します。

        Args:
            db (AsyncSession): 非同期データベースセッション。
            user (User): 作成するユーザーオブジェクト。

        Returns:
            User: 作成されたユーザーオブジェクト。
        """
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user