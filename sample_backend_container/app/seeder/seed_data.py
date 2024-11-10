# seed_data.py
# このスクリプトは開発用のデータ投入用スクリプトです。
# 初期データをデータベースに挿入して動作確認することが目的。
# poetry run python app/seeder/seed_data.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# NOTE: app.modelsをインポートする方法がもうちょっといい方法がないのか？？
import sys
from pathlib import Path
# プロジェクトのルートディレクトリをモジュール検索パスに追加
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
import app.models  # インポート可能にする

# alembic.iniファイルを読み込む
import configparser

config = configparser.ConfigParser()
config.read('alembic.ini')  # alembic.iniのパスは適宜調整

# sqlalchemy.urlの値を取得
DATABASE_URL = config.get('alembic', 'sqlalchemy.url')

# 同期的なエンジンとセッションの作成
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def seed_data():
    # 同期セッションを使用してデータベース接続を管理
    session = SessionLocal()

    try:
        # SampleModelの初期データ
        # "Initial Sample 1"というnameを持つレコードが存在しない場合のみ、新しいレコードを追加
        if (
            not session.query(app.models.SampleModel)
            .filter_by(name="Initial Sample 1")
            .first()
        ):
            session.add(
                app.models.SampleModel(
                    name="Initial Sample 1", description="Description for Sample 1"
                )
            )

        # SampleModel2の初期データ
        # "Initial SampleModel2"というnameを持つレコードが存在しない場合のみ、新しいレコードを追加
        if (
            not session.query(app.models.SampleModel2)
            .filter_by(name="Initial SampleModel2")
            .first()
        ):
            session.add(
                app.models.SampleModel2(
                    name="Initial SampleModel2",
                    description="Description for SampleModel2",
                    related_id=1,
                )
            )

        # SampleModel3の初期データ
        # "Initial SampleModel3"というnamesssを持つレコードが存在しない場合のみ、新しいレコードを追加
        if (
            not session.query(app.models.SampleModel3)
            .filter_by(namesss="Initial SampleModel3")
            .first()
        ):
            session.add(
                app.models.SampleModel3(
                    namesss="Initial SampleModel3",
                    descriptionsss="Description for SampleModel3",
                )
            )

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
