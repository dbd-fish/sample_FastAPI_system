from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from app.core.log_config import logger, structlog

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
