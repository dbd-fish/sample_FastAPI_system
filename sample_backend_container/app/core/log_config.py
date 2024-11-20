import logging
from logging.handlers import TimedRotatingFileHandler
import structlog
import os
from datetime import datetime

# ログディレクトリ
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

# 現在の日付を取得してファイル名に含める
def get_log_file_name():
    current_date = datetime.now().strftime("%Y-%m-%d")
    return os.path.join(log_dir, f"app_{current_date}.log")

# 初期ログファイル名
log_file_path = get_log_file_name()

# loggingの設定
file_handler = TimedRotatingFileHandler(
    filename=log_file_path,  # ファイルパス
    when="midnight",         # 毎日深夜にログローテーション
    interval=1,              # 1日ごと
    backupCount=7,           # 古いログファイルを7つ保持
    encoding="utf-8"         # エンコーディング設定
)

# ログファイル名を更新するためにタイムスタンプ付きの拡張子をカスタマイズ
file_handler.namer = lambda name: name.replace(".log", "") + f"_{datetime.now().strftime('%Y-%m-%d')}.log"

# logging.basicConfigをカスタムハンドラーで設定
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        file_handler,         # 日付ごとのファイル出力
        logging.StreamHandler(),  # コンソール出力
    ],
)

# structlogの設定
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

# structlogのロガー作成
logger = structlog.get_logger()
