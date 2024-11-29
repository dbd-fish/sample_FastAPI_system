import logging
import structlog
import os
from datetime import datetime
from zoneinfo import ZoneInfo
from structlog.processors import CallsiteParameter
from app.config.setting import setting


def create_log_directory(directory: str) -> None:
    """
    指定されたログディレクトリを作成します。

    Args:
        directory (str): 作成するログディレクトリのパス。
    """
    os.makedirs(directory, exist_ok=True)


def get_log_file_path(directory: str, filename_template: str = "app_{date}.log") -> str:
    """
    現在の日付を基にログファイルのパスを生成します。

    Args:
        directory (str): ログファイルを保存するディレクトリ。
        filename_template (str): ログファイル名のテンプレート。

    Returns:
        str: 生成されたログファイルのフルパス。
    """
    current_date = datetime.now(ZoneInfo("Asia/Tokyo")).strftime("%Y-%m-%d")
    return os.path.join(directory, filename_template.format(date=current_date))


def configure_logging(test_env: int = 0) -> structlog.BoundLogger:
    """
    ログ設定を行います。ファイルハンドラーやカスタムフォーマッタの設定、
    structlog用のプロセッサを含みます。

    Args:
        test_env (int): テスト環境の指定。
            0: 本番環境
            1: 単体テスト環境
            2: 結合テスト環境
    Returns:
        structlog.BoundLogger: 設定済みのstructlogロガーインスタンス。
    """
    # アプリケーションログの設定
    if test_env==1:
        # 単体テストの場合
        create_log_directory(setting.UT_APP_LOG_DIRECTORY)
        app_log_file_path = get_log_file_path(setting.UT_APP_LOG_DIRECTORY)
    elif test_env==2:
        # 結合テストの場合
        create_log_directory(setting.IT_APP_LOG_DIRECTORY)
        app_log_file_path = get_log_file_path(setting.IT_APP_LOG_DIRECTORY)
    else:
        # 通常のサーバー起動の場合　test_env==0
        create_log_directory(setting.APP_LOG_DIRECTORY)
        app_log_file_path = get_log_file_path(setting.APP_LOG_DIRECTORY)

    # 日本時間対応のカスタムフォーマッタ
    class JSTFormatter(logging.Formatter):
        """
        日本時間（JST）でタイムスタンプをフォーマットするカスタムフォーマッタ。
        """
        def formatTime(self, record, datefmt=None):
            """
            ログレコードのタイムスタンプをJSTでフォーマットします。

            Args:
                record (logging.LogRecord): ログレコード。
                datefmt (Optional[str]): 日付フォーマット文字列。

            Returns:
                str: フォーマットされたタイムスタンプ。
            """
            dt = datetime.fromtimestamp(record.created, ZoneInfo("Asia/Tokyo"))
            if datefmt:
                return dt.strftime(datefmt)
            return dt.isoformat()

    # アプリケーションログのファイルハンドラ設定
    app_file_handler = logging.FileHandler(app_log_file_path, encoding="utf-8")
    app_file_handler.setLevel(logging.INFO)
    app_formatter = JSTFormatter("[%(asctime)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    app_file_handler.setFormatter(app_formatter)

    # アプリケーション用のロガー設定
    app_logger = logging.getLogger("app")
    app_logger.handlers = []
    app_logger.setLevel(logging.INFO)
    app_logger.addHandler(app_file_handler)

    # SQLAlchemyログの設定
    sqlalchemy_logger = logging.getLogger('sqlalchemy.engine')
    if test_env in [1, 2]:
        # 単体テストまたは結合テスト環境の場合、SQLAlchemyのログを無効化
        sqlalchemy_logger.setLevel(logging.WARNING)
    else:
        # 本番環境の場合、通常のログ設定
        configure_sqlalchemy_logging(test_env)

    # structlogの設定
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,  # リクエストスコープでの変数をログに統合
            structlog.processors.TimeStamper(fmt="iso", utc=False),  # ISOフォーマットのタイムスタンプを追加
            structlog.processors.add_log_level,  # ログレベルを追加
            structlog.stdlib.add_logger_name,  # ロガー名を追加
            structlog.processors.format_exc_info,  # 例外情報をフォーマット
            structlog.processors.CallsiteParameterAdder(  # ログ発生箇所の情報を追加
                [
                    CallsiteParameter.PATHNAME,  # ファイルのパス
                    # CallsiteParameter.MODULE,  # モジュール名
                    CallsiteParameter.FUNC_NAME,  # 関数名
                    CallsiteParameter.LINENO,  # 行番号
                ]
            ),
            structlog.processors.JSONRenderer(indent=4, sort_keys=True),  # JSON形式で出力
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # 設定済みのロガーを返却
    return structlog.get_logger()


def configure_sqlalchemy_logging(test_env: int = 0) -> None:
    """
    SQLAlchemyのログ設定を行います。
    """
    # SQLAlchemyログの設定
    if test_env==0:
        create_log_directory(setting.SQL_LOG_DIRECTORY)
        sqlalchemy_log_file_path = get_log_file_path(setting.SQL_LOG_DIRECTORY, "sqlalchemy_{date}.log")
    elif test_env==1:
        create_log_directory(setting.UT_SQL_LOG_DIRECTORY)
        sqlalchemy_log_file_path = get_log_file_path(setting.UT_SQL_LOG_DIRECTORY, "sqlalchemy_{date}.log")
    elif test_env==2:
        create_log_directory(setting.IT_SQL_LOG_DIRECTORY)
        sqlalchemy_log_file_path = get_log_file_path(setting.IT_SQL_LOG_DIRECTORY, "sqlalchemy_{date}.log")

    # SQLAlchemy専用ロガーを設定
    sqlalchemy_logger = logging.getLogger("sqlalchemy.engine")
    sqlalchemy_logger.handlers = []
    sqlalchemy_logger.setLevel(logging.INFO)

    # SQLAlchemy用のファイルハンドラ
    sqlalchemy_file_handler = logging.FileHandler(sqlalchemy_log_file_path, encoding="utf-8")
    sqlalchemy_formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
    sqlalchemy_file_handler.setFormatter(sqlalchemy_formatter)

    # ハンドラをロガーに追加
    sqlalchemy_logger.addHandler(sqlalchemy_file_handler)

    # アプリケーションログから除外
    sqlalchemy_logger.propagate = False


# ロガー作成
logger = configure_logging()
