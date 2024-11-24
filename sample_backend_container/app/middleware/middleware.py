from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from app.core.log_config import logger, structlog
from fastapi import Request, HTTPException
from starlette.responses import JSONResponse
import structlog

# ロガーの設定
logger = structlog.get_logger()

class AddUserIPMiddleware(BaseHTTPMiddleware):
    """
    リクエストのIPアドレスをログに記録するミドルウェア。
    """
    async def dispatch(self, request: Request, call_next):
        user_ip = request.client.host
        structlog.contextvars.bind_contextvars(user_ip=user_ip)
        logger.info("User IP in Middleware", user_ip=user_ip)
        try:
            response = await call_next(request)
        finally:
            structlog.contextvars.clear_contextvars()
        return response

class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """
    エラーハンドリング用ミドルウェア。
    リクエスト処理中に発生した例外をキャッチし、適切なレスポンスを返します。
    """
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except HTTPException as http_exc:
            logger.warning(
                "HTTPException occurred",
                detail=http_exc.detail,
                status_code=http_exc.status_code,
                user_ip=request.client.host
            )
            return JSONResponse(
                status_code=http_exc.status_code,
                content={"message": http_exc.detail},
                headers=http_exc.headers,
            )
        except Exception as exc:
            logger.error(
                "Unhandled exception occurred",
                error=str(exc),
                user_ip=request.client.host,
                path=request.url.path,
                method=request.method,
            )
            return JSONResponse(
                status_code=500,
                content={"message": "Internal Server Error"},
            )