# seed_data.py
# このスクリプトは開発用のデータ投入用スクリプトです。
# 初期データをデータベースに挿入して動作確認することが目的です。
# 実行コマンド: 
# export PYTHONPATH=/app
# poetry run python app/seeder/seed_data.py

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.future import select
from datetime import datetime
from pathlib import Path
import configparser
import sys
import asyncio
from app.core.config import TestData
from app.common.common import datetime_now
from passlib.context import CryptContext
from sqlalchemy.sql import text


# プロジェクトのルートディレクトリをモジュール検索パスに追加
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
import app.models  # すべてのモデルをインポート

# alembic.iniファイルを読み込む
config = configparser.ConfigParser()
config.read("alembic.ini")

# 非同期エンジン用のDATABASE_URLを取得
DATABASE_URL = config.get("alembic", "sqlalchemy.url")

# 非同期エンジンとセッションの作成
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(bind=engine, autoflush=False, autocommit=False)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
async def clear_data():
    """
    データベース内の全データをクリアします。
    外部キー制約を無効化して削除後、元に戻します。
    """
    async with AsyncSessionLocal() as session:
        try:
            # 外部キー制約を無効化
            await session.execute(text("SET session_replication_role = 'replica';"))
            
            # 削除対象のテーブルリスト
            tables_to_clear = [
                "user_view_history",
                "report_view_history",
                "tag_view_history",
                "report_comment_history",
                "group_evaluation_history",
                "user_search_history",
                "group_search_history",
                "group_evaluation",
                "report_evaluation_history",
                "user_evaluation_history",
                "report_supplement",
                "report_tag_link",
                "report_tag",
                "report",
                "user_group_membership",
                "group_profile",
                "user_group",
                "user_ip_address",
                "user_profile",
                '"user"'  # 修正: userテーブルを二重引用符で囲む
            ]

            # 各テーブルのデータを削除
            for table in tables_to_clear:
                print(f"Clearing table: {table}")
                await session.execute(text(f"TRUNCATE TABLE {table} CASCADE;"))

            # 外部キー制約を元に戻す
            await session.execute(text("SET session_replication_role = 'origin';"))
            await session.commit()
            print("Database cleared successfully.")

        except Exception as e:
            await session.rollback()
            print(f"An error occurred while clearing data: {e}")
        finally:
            await session.close()


async def seed_data():
    async with AsyncSessionLocal() as session:
        try:
            # 固定値のUUIDやIDを定義
            user1_id = TestData.TEST_USER_ID_1
            user2_id = TestData.TEST_USER_ID_2
            group_id = TestData.TEST_GROUP_ID
            report_id = TestData.TEST_REPORT_ID
            tag_id = 1

            # 1. Userテーブル
            result = await session.execute(
                select(app.models.User).where(app.models.User.username == "testuser")
            )
            if not result.scalars().first():
                session.add(
                    app.models.User(
                        user_id=user1_id,
                        username="testuser",
                        email="testuser@example.com",
                        password_hash=pwd_context.hash("password"),
                        contact_number="123456789",
                        user_role=1,
                        user_status=1,
                        created_at=datetime_now(),
                        updated_at=datetime_now(),
                    )
                )
            await session.commit()

            # 1. Userテーブル (target_user_id 用のデータ追加)
            result = await session.execute(
                select(app.models.User).where(app.models.User.username == "targetuser")
            )
            if not result.scalars().first():
                session.add(
                    app.models.User(
                        user_id=user2_id,
                        username="targetuser",
                        email="targetuser@example.com",
                        password_hash=pwd_context.hash("password"),
                        contact_number="987654321",
                        user_role=2,
                        user_status=1,
                        created_at=datetime_now(),
                        updated_at=datetime_now(),
                    )
                )
            await session.commit()


            # 2. UserProfileテーブル
            result = await session.execute(
                select(app.models.UserProfile).where(app.models.UserProfile.display_name == "Test User")
            )
            if not result.scalars().first():
                session.add(
                    app.models.UserProfile(
                        profile_id=1,
                        user_id=user1_id,
                        display_name="Test User",
                        profile_text="This is a test user profile.",
                        profile_image_url="http://example.com/image.png",
                        created_at=datetime_now(),
                        updated_at=datetime_now(),
                    )
                )
            await session.commit()

            # 3. UserIPAddressテーブル
            result = await session.execute(
                select(app.models.UserIPAddress).where(app.models.UserIPAddress.ip_address == "192.168.0.1")
            )
            if not result.scalars().first():
                session.add(
                    app.models.UserIPAddress(
                        ip_id=1,
                        user_id=user1_id,
                        ip_address="192.168.0.1",
                        created_at=datetime_now(),
                        updated_at=datetime_now(),
                    )
                )
            await session.commit()

            # 4. UserGroupテーブル
            result = await session.execute(
                select(app.models.UserGroup).where(app.models.UserGroup.group_name == "Sample Group")
            )
            if not result.scalars().first():
                session.add(
                    app.models.UserGroup(
                        group_id=group_id,
                        group_name="Sample Group",
                        created_at=datetime_now(),
                        updated_at=datetime_now(),
                    )
                )
            await session.commit()

            # 5. GroupProfileテーブル
            result = await session.execute(
                select(app.models.GroupProfile).where(app.models.GroupProfile.display_name == "Sample Group Display")
            )
            if not result.scalars().first():
                session.add(
                    app.models.GroupProfile(
                        profile_id=1,
                        group_id=group_id,
                        display_name="Sample Group Display",
                        profile_text="This is a sample group profile.",
                        profile_image_url="http://example.com/group_image.png",
                        created_at=datetime_now(),
                        updated_at=datetime_now(),
                    )
                )
            await session.commit()

            # 6. UserGroupMembershipテーブル
            result = await session.execute(
                select(app.models.UserGroupMembership).where(
                    (app.models.UserGroupMembership.user_id == user1_id)
                    & (app.models.UserGroupMembership.group_id == group_id)
                )
            )
            if not result.scalars().first():
                session.add(
                    app.models.UserGroupMembership(
                        user_id=user1_id,
                        group_id=group_id,
                        created_at=datetime_now(),
                        updated_at=datetime_now(),
                    )
                )
            await session.commit()

            # 7. Reportテーブル
            result = await session.execute(
                select(app.models.Report).where(app.models.Report.title == "Sample Report")
            )
            if not result.scalars().first():
                session.add(
                    app.models.Report(
                        report_id=report_id,
                        user_id=user1_id,
                        title="Sample Report",
                        content="This is a sample report.",
                        format=1,  # markdown
                        visibility=3,  # private
                        created_at=datetime_now(),
                        updated_at=datetime_now(),
                    )
                )
            await session.commit()

            # 8. ReportTagテーブル
            result = await session.execute(
                select(app.models.ReportTag).where(app.models.ReportTag.tag_name == "Sample Tag")
            )
            if not result.scalars().first():
                session.add(
                    app.models.ReportTag(
                        tag_id=tag_id,
                        tag_name="Sample Tag",
                        created_at=datetime_now(),
                        updated_at=datetime_now(),
                    )
                )
            await session.commit()

            # 9. ReportTagLinkテーブル
            result = await session.execute(
                select(app.models.ReportTagLink).where(app.models.ReportTagLink.report_id == report_id)
            )
            if not result.scalars().first():
                session.add(
                    app.models.ReportTagLink(
                        report_id=report_id,
                        tag_id=tag_id,
                        created_at=datetime_now(),
                        updated_at=datetime_now(),
                    )
                )
            await session.commit()

            # 10. ReportSupplementテーブル
            result = await session.execute(
                select(app.models.ReportSupplement).where(app.models.ReportSupplement.report_id == report_id)
            )
            report_supplement = result.scalars().first()
            if not report_supplement:
                session.add(
                    app.models.ReportSupplement(
                        report_supplement=1,
                        report_id=report_id,
                        user_id=user1_id,
                        content="Supplement to the sample report",
                        start_report=0,
                        end_report=10,
                        supplement_url="http://example.com/supplement",
                        created_at=datetime_now(),
                        updated_at=datetime_now(),
                    )
                )
                await session.commit()

            # 11. UserEvaluationHistoryテーブル
            result = await session.execute(
                select(app.models.UserEvaluationHistory).where(app.models.UserEvaluationHistory.eval_id == 1)
            )
            if not result.scalars().first():
                session.add(
                    app.models.UserEvaluationHistory(
                        eval_id=1,
                        user_id=user1_id,
                        target_user_id=user2_id,
                        score=5,
                        comment="Great user!",
                        created_at=datetime_now(),
                        updated_at=datetime_now(),
                    )
                )
            await session.commit()

            # 12. ReportEvaluationHistoryテーブル
            result = await session.execute(
                select(app.models.ReportEvaluationHistory).where(app.models.ReportEvaluationHistory.eval_id == 1)
            )
            if not result.scalars().first():
                session.add(
                    app.models.ReportEvaluationHistory(
                        eval_id=1,
                        user_id=user1_id,
                        report_id=report_id,
                        score=4,
                        comment="Great report!",
                        created_at=datetime_now(),
                        updated_at=datetime_now(),
                    )
                )
            await session.commit()

            # 13. GroupEvaluationテーブル
            result = await session.execute(
                select(app.models.GroupEvaluation).where(app.models.GroupEvaluation.eval_id == 1)
            )
            if not result.scalars().first():
                session.add(
                    app.models.GroupEvaluation(
                        eval_id=1,
                        evaluator_id=user1_id,
                        group_id=group_id,
                        score=85,
                        comment="Good performance",
                        created_at=datetime_now(),
                        updated_at=datetime_now(),
                    )
                )
            await session.commit()

            # 14. ReportCommentHistoryテーブル
            result = await session.execute(
                select(app.models.ReportCommentHistory).where(app.models.ReportCommentHistory.history_id == 1)
            )
            if not result.scalars().first():
                session.add(
                    app.models.ReportCommentHistory(
                        history_id=1,
                        report_supplement=1, 
                        user_id=user1_id,
                        report_id=report_id,
                        content="This is a comment",
                        report_supplement_action=1,  # created
                        created_at=datetime_now(),
                        updated_at=datetime_now(),
                    )
                )
            await session.commit()

            # 15. TagViewHistoryテーブル
            result = await session.execute(
                select(app.models.TagViewHistory).where(app.models.TagViewHistory.user_id == user1_id)
            )
            if not result.scalars().first():
                session.add(
                    app.models.TagViewHistory(
                        user_id=user1_id,
                        tag_id=tag_id,
                        view_date=datetime_now(),
                        created_at=datetime_now(),
                        updated_at=datetime_now(),
                    )
                )
            await session.commit()

            # 16. ReportViewHistoryテーブル
            result = await session.execute(
                select(app.models.ReportViewHistory).where(app.models.ReportViewHistory.user_id == user1_id)
            )
            if not result.scalars().first():
                session.add(
                    app.models.ReportViewHistory(
                        user_id=user1_id,
                        report_id=report_id,
                        view_date=datetime_now(),
                        created_at=datetime_now(),
                        updated_at=datetime_now(),
                    )
                )
            await session.commit()

            # 17. UserViewHistoryテーブル
            result = await session.execute(
                select(app.models.UserViewHistory).where(app.models.UserViewHistory.viewer_user_id == user1_id)
            )
            if not result.scalars().first():
                session.add(
                    app.models.UserViewHistory(
                        viewer_user_id=user1_id,
                        viewed_user_id=user2_id,
                        view_date=datetime_now(),
                        created_at=datetime_now(),
                        updated_at=datetime_now(),
                    )
                )
            await session.commit()

            # 18. UserSearchHistoryテーブル
            result = await session.execute(
                select(app.models.UserSearchHistory).where(app.models.UserSearchHistory.user_id == user1_id)
            )
            if not result.scalars().first():
                session.add(
                    app.models.UserSearchHistory(
                        user_id=user1_id,
                        search_term="Sample search",
                        search_date=datetime_now(),
                        created_at=datetime_now(),
                        updated_at=datetime_now(),
                    )
                )
            await session.commit()

            # 19. GroupSearchHistoryテーブル
            result = await session.execute(
                select(app.models.GroupSearchHistory).where(app.models.GroupSearchHistory.user_id == user1_id)
            )
            if not result.scalars().first():
                session.add(
                    app.models.GroupSearchHistory(
                        user_id=user1_id,
                        search_term="Sample group search",
                        search_date=datetime_now(),
                        created_at=datetime_now(),
                        updated_at=datetime_now(),
                    )
                )
            await session.commit()

            # 20. GroupEvaluationHistoryテーブル
            result = await session.execute(
                select(app.models.GroupEvaluationHistory).where(app.models.GroupEvaluationHistory.eval_id == 1)
            )
            if not result.scalars().first():
                session.add(
                    app.models.GroupEvaluationHistory(
                        eval_id=1,
                        evaluator_id=user1_id,
                        group_id=group_id,
                        score=4,
                        comment="Excellent group",
                        created_at=datetime_now(),
                        updated_at=datetime_now(),
                    )
                )
            await session.commit()

            print("Data seeded successfully!")

        except Exception as e:
            await session.rollback()
            print(f"An error occurred: {e}")
        finally:
            await session.close()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Seed or clear database.")
    parser.add_argument("--clear", action="store_true", help="Clear all database data")
    args = parser.parse_args()

    if args.clear:
        print("Clearing database...")
        asyncio.run(clear_data())
    else:
        print("Seeding database...")
        asyncio.run(seed_data())
