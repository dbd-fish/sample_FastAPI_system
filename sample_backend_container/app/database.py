from sqlalchemy.ext.declarative import declarative_base  #
import configparser
from databases import Database

# alembic.iniファイルからDB接続
config = configparser.ConfigParser()
config.read('alembic.ini')  # alembic.iniのパスは適宜調整
DATABASE_URL = config.get('alembic', 'sqlalchemy.url')
# Databasesパッケージの設定
database = Database(DATABASE_URL)

# Baseクラスの定義
Base = declarative_base()