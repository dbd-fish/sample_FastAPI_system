from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
from starlette.responses import JSONResponse
from app.core.log_config import logger, structlog

# ロガーの設定
logger = structlog.get_logger()

class AddUserIPMiddleware(BaseHTTPMiddleware):
    """
    リクエストのIPアドレスをログに記録するミドルウェア。
    ユーザーのIPアドレスをリクエストごとに取得し、ログに記録。
    """

    async def dispatch(self, request: Request, call_next):
        """
        ミドルウェアのメイン処理。リクエストのIPアドレスをログに記録し、
        ログのコンテキストにバインドします。

        Args:
            request (Request): FastAPIのリクエストオブジェクト。
            call_next (Callable): 次のミドルウェアまたはエンドポイントを呼び出す関数。

        Returns:
            Response: リクエストのレスポンスオブジェクト。
        """
        user_ip = request.client.host  # クライアントのIPアドレスを取得
        structlog.contextvars.bind_contextvars(user_ip=user_ip)  # ログコンテキストにIPアドレスをバインド
        logger.info("User IP in Middleware", user_ip=user_ip)  # IPアドレスをログに記録
        try:
            # 次の処理を実行
            response = await call_next(request)
        finally:
            # リクエストごとのログコンテキストをクリア
            structlog.contextvars.clear_contextvars()
        return response


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """
    エラーハンドリング用ミドルウェア。
    リクエスト処理中に発生した例外をキャッチし、適切なレスポンスを返します。
    """

    async def dispatch(self, request: Request, call_next):
        """
        ミドルウェアのメイン処理。HTTPExceptionと一般的な例外をキャッチし、
        適切なログ記録とレスポンスを返します。

        Args:
            request (Request): FastAPIのリクエストオブジェクト。
            call_next (Callable): 次のミドルウェアまたはエンドポイントを呼び出す関数。

        Returns:
            Response: エラーレスポンスまたはリクエストのレスポンスオブジェクト。
        """
        try:
            # 次の処理を実行
            response = await call_next(request)
            return response
        except HTTPException as http_exc:
            # HTTPExceptionをキャッチした場合の処理
            logger.warning(
                "HTTPException occurred",  # 警告ログ
                detail=http_exc.detail,  # エラー詳細
                status_code=http_exc.status_code,  # HTTPステータスコード
                user_ip=request.client.host,  # ユーザーのIPアドレス
            )
            # HTTPExceptionに基づいてJSONレスポンスを返す
            return JSONResponse(
                status_code=http_exc.status_code,
                content={"message": http_exc.detail},  # エラー詳細を返す
                headers=http_exc.headers,
            )
        except Exception as exc:
            # 予期しない例外をキャッチした場合の処理
            logger.error(
                "Unhandled exception occurred",  # エラーログ
                error=str(exc),  # 例外の内容
                user_ip=request.client.host,  # ユーザーのIPアドレス
                path=request.url.path,  # リクエストされたURLパス
                method=request.method,  # リクエストメソッド（GET, POSTなど）
            )
            # 一般的な500エラーを返す
            return JSONResponse(
                status_code=500,
                content={"message": "Internal Server Error"},  # エラーメッセージ
            )
