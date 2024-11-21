import logging
import structlog
import os
from datetime import datetime
from zoneinfo import ZoneInfo
from structlog.processors import CallsiteParameter

# ログディレクトリ作成
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

# 現在の日付を取得してログファイル名を生成
def get_log_file_name():
    current_date = datetime.now(ZoneInfo("Asia/Tokyo")).strftime("%Y-%m-%d")
    return os.path.join(log_dir, f"app_{current_date}.log")

log_file_path = get_log_file_name()

# 日本時間対応のカスタムフォーマッタ
class JSTFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created, ZoneInfo("Asia/Tokyo"))
        if datefmt:
            return dt.strftime(datefmt)
        return dt.isoformat()

file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
file_handler.setLevel(logging.INFO)
formatter = JSTFormatter("[%(asctime)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
file_handler.setFormatter(formatter)

logging.basicConfig(
    handlers=[file_handler],
    level=logging.INFO,
)

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.TimeStamper(fmt="iso", utc=False),
        structlog.processors.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.format_exc_info,
        structlog.processors.CallsiteParameterAdder(
            [
                CallsiteParameter.PATHNAME,
                CallsiteParameter.MODULE,
                CallsiteParameter.FUNC_NAME,
                CallsiteParameter.LINENO,
            ]
        ),
        structlog.processors.JSONRenderer(indent=4, sort_keys=True),
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)
# structlogのロガー作成
logger = structlog.get_logger()
