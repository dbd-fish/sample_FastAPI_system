# seed_data.py
# このスクリプトは開発用のデータ投入用スクリプトです。
# 初期データをデータベースに挿入して動作確認することが目的です。
# 実行コマンド: poetry run python app/seeder/seed_data.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
from pathlib import Path
import configparser
from datetime import datetime  # 現在の日時を取得するためにdatetimeをインポート

# プロジェクトのルートディレクトリをモジュール検索パスに追加
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
import app.models  # すべてのモデルをインポート

# alembic.iniファイルを読み込む
config = configparser.ConfigParser()
config.read('alembic.ini')

# sqlalchemy.urlの値を取得
DATABASE_URL = config.get('alembic', 'sqlalchemy.url')

# 同期的なエンジンとセッションの作成
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def seed_data():
    # 同期セッションを使用してデータベース接続を管理
    session = SessionLocal()

    try:
        
        # Userテーブルの初期データ
        if not session.query(app.models.User).filter_by(username="testuser").first():
            session.add(app.models.User(
                user_id="sample-uuid-1234",
                username="testuser",
                email="testuser@example.com",
                password_hash="hashed_password",
                contact_number="123456789",
                user_role=1,
                user_status=1,
                created_at=datetime.now(),
                updated_at=datetime.now()
            ))
        session.commit()
        
        # target_user_id用の追加ユーザーを作成
        if not session.query(app.models.User).filter_by(user_id="sample-uuid-1235").first():
            session.add(app.models.User(
                user_id="sample-uuid-1235",
                username="targetuser",
                email="targetuser@example.com",
                password_hash="hashed_password",
                contact_number="987654321",
                user_role=2,
                user_status=1,
                created_at=datetime.now(),
                updated_at=datetime.now()
            ))

        # Userの挿入をコミット
        session.commit()


        # UserProfileテーブルの初期データ
        if not session.query(app.models.UserProfile).filter_by(display_name="Test User").first():
            session.add(app.models.UserProfile(
                profile_id=1,
                user_id="sample-uuid-1234",
                display_name="Test User",
                profile_text="This is a test user profile.",
                profile_image_url="http://example.com/image.png",
                created_at=datetime.now(),
                updated_at=datetime.now()
            ))
        session.commit()
        
        # UserIPAddressテーブルの初期データ
        if not session.query(app.models.UserIPAddress).filter_by(ip_address="192.168.0.1").first():
            session.add(app.models.UserIPAddress(
                ip_id=1,
                user_id="sample-uuid-1234",
                ip_address="192.168.0.1",
                created_at=datetime.now(),
                updated_at=datetime.now()
            ))
        session.commit()
        
        # UserGroupテーブルの初期データ
        if not session.query(app.models.UserGroup).filter_by(group_name="Sample Group").first():
            session.add(app.models.UserGroup(
                group_id="sample-group-uuid",
                group_name="Sample Group",
                created_at=datetime.now(),
                updated_at=datetime.now()
            ))
        session.commit()
        
        # GroupProfileテーブルの初期データ
        if not session.query(app.models.GroupProfile).filter_by(display_name="Sample Group Display").first():
            session.add(app.models.GroupProfile(
                profile_id=1,
                group_id="sample-group-uuid",
                display_name="Sample Group Display",
                profile_text="This is a sample group profile.",
                profile_image_url="http://example.com/group_image.png",
                created_at=datetime.now(),
                updated_at=datetime.now()
            ))
        session.commit()
        
        # UserGroupMembershipテーブルの初期データ
        if not session.query(app.models.UserGroupMembership).filter_by(user_id="sample-uuid-1234", group_id="sample-group-uuid").first():
            session.add(app.models.UserGroupMembership(
                user_id="sample-uuid-1234",
                group_id="sample-group-uuid",
                created_at=datetime.now(),
                updated_at=datetime.now()
            ))
        session.commit()
        
        # Reportテーブルの初期データ
        if not session.query(app.models.Report).filter_by(title="Sample Report").first():
            session.add(app.models.Report(
                report_id="sample-report-uuid",
                user_id="sample-uuid-1234",
                title="Sample Report",
                content="This is a sample report.",
                format=1,  # markdown
                visibility=3,  # private
                created_at=datetime.now(),
                updated_at=datetime.now()
            ))
        session.commit()
        
        # ReportTagテーブルの初期データ
        if not session.query(app.models.ReportTag).filter_by(tag_name="Sample Tag").first():
            session.add(app.models.ReportTag(
                tag_id=1,
                tag_name="Sample Tag",
                created_at=datetime.now(),
                updated_at=datetime.now()
            ))
        session.commit()
        
        # ReportTagLinkテーブルの初期データ
        if not session.query(app.models.ReportTagLink).filter_by(report_id="sample-report-uuid").first():
            session.add(app.models.ReportTagLink(
                report_id="sample-report-uuid",
                tag_id=1,
                created_at=datetime.now(),
                updated_at=datetime.now()
            ))
        session.commit()
        
        # ReportSupplementテーブルの初期データ
        if not session.query(app.models.ReportSupplement).filter_by(report_id="sample-report-uuid").first():
            session.add(app.models.ReportSupplement(
                report_supplement=1,
                report_id="sample-report-uuid",
                user_id="sample-uuid-1234",
                content="This is a supplement to the sample report.",
                start_report=0,
                end_report=10,
                supplement_url="http://example.com/supplement",
                created_at=datetime.now(),
                updated_at=datetime.now()
            ))
        session.commit()
        
        # UserEvaluationHistoryテーブルの初期データ
        if not session.query(app.models.UserEvaluationHistory).filter_by(eval_id=1).first():
            session.add(app.models.UserEvaluationHistory(
                eval_id=1,
                user_id="sample-uuid-1234",
                target_user_id="sample-uuid-1235",
                score=5,
                comment="Good job",
                created_at=datetime.now(),
                updated_at=datetime.now()
            ))
        session.commit()
        
        # ReportEvaluationHistoryテーブルの初期データ
        if not session.query(app.models.ReportEvaluationHistory).filter_by(eval_id=1).first():
            session.add(app.models.ReportEvaluationHistory(
                eval_id=1,
                user_id="sample-uuid-1234",
                report_id="sample-report-uuid",
                score=4,
                comment="Great report!",
                created_at=datetime.now(),
                updated_at=datetime.now()
            ))
        session.commit()
        
        # GroupEvaluationHistoryテーブルの初期データ
        if not session.query(app.models.GroupEvaluationHistory).filter_by(eval_id=1).first():
            session.add(app.models.GroupEvaluationHistory(
                eval_id=1,
                evaluator_id="sample-uuid-1234",
                group_id="sample-group-uuid",
                score=4,
                comment="Excellent group",
                created_at=datetime.now(),
                updated_at=datetime.now()
            ))
        session.commit()
        
        # ReportCommentHistoryテーブルの初期データ
        if not session.query(app.models.ReportCommentHistory).filter_by(history_id=1).first():
            session.add(app.models.ReportCommentHistory(
                report_supplement=1,
                user_id="sample-uuid-1234",
                report_id="sample-report-uuid",
                content="This is a comment",
                report_supplement_action=1,  # created
                created_at=datetime.now(),
                updated_at=datetime.now()
            ))
        session.commit()
        
        # TagViewHistoryテーブルの初期データ
        if not session.query(app.models.TagViewHistory).filter_by(user_id="sample-uuid-1234").first():
            session.add(app.models.TagViewHistory(
                user_id="sample-uuid-1234",
                tag_id=1,
                view_date=datetime.now(), 
                created_at=datetime.now(),
                updated_at=datetime.now()
            ))
        session.commit()
        
        # GroupEvaluationテーブルの初期データ
        if not session.query(app.models.GroupEvaluation).filter_by(group_id="sample-group-uuid").first():
            session.add(app.models.GroupEvaluation(
                eval_id=1,
                evaluator_id="sample-uuid-1234",
                group_id="sample-group-uuid",
                score=85,
                comment="Good performance",
                created_at=datetime.now(),
                updated_at=datetime.now()
            ))
        session.commit()
        
        # ReportViewHistoryテーブルの初期データ
        if not session.query(app.models.ReportViewHistory).filter_by(user_id="sample-uuid-1234").first():
            session.add(app.models.ReportViewHistory(
                user_id="sample-uuid-1234",
                report_id="sample-report-uuid",
                view_date=datetime.now(),
                created_at=datetime.now(),
                updated_at=datetime.now()
            ))
        session.commit()
        
        # UserViewHistoryテーブルの初期データ
        if not session.query(app.models.UserViewHistory).filter_by(viewer_id="sample-uuid-1234").first():
            session.add(app.models.UserViewHistory(
                viewer_id="sample-uuid-1234",
                viewed_user_id="sample-uuid-1235",
                view_date=datetime.now(),
                created_at=datetime.now(),
                updated_at=datetime.now()
            ))
        session.commit()
        
        # UserSearchHistoryテーブルの初期データ
        if not session.query(app.models.UserSearchHistory).filter_by(user_id="sample-uuid-1234").first():
            session.add(app.models.UserSearchHistory(
                user_id="sample-uuid-1234",
                search_term="Sample search",
                search_date=datetime.now(),
                created_at=datetime.now(),
                updated_at=datetime.now()
            ))
        session.commit()
        
        # GroupSearchHistoryテーブルの初期データ
        if not session.query(app.models.GroupSearchHistory).filter_by(user_id="sample-uuid-1234").first():
            session.add(app.models.GroupSearchHistory(
                user_id="sample-uuid-1234",
                search_term="Sample group search",
                search_date=datetime.now(),
                created_at=datetime.now(),
                updated_at=datetime.now()
            ))

        # コミットして変更を保存
        session.commit()
        print("Data seeded successfully!")

    except Exception as e:
        # エラー発生時にロールバック
        session.rollback()
        print(f"An error occurred: {e}")
    finally:
        # セッションを閉じてリソースを解放
        session.close()


if __name__ == "__main__":
    seed_data()
