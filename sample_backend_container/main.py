from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from app.database import database
from app.routes import router
from app.core.log_config import logger, structlog
from contextlib import asynccontextmanager
from fastapi import Request

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    アプリケーションのライフサイクル管理。
    """
    # アプリケーション起動時の処理
    logger.info("Application startup - connecting to database.")
    await database.connect()
    yield
    # アプリケーション終了時の処理
    logger.info("Application shutdown - disconnecting from database.")
    await database.disconnect()

# FastAPIアプリケーションインスタンスを作成し、lifespanを設定
app = FastAPI(lifespan=lifespan)

# IPアドレスをログに追加するミドルウェア
class AddUserIPMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        user_ip = request.client.host
        structlog.contextvars.bind_contextvars(user_ip=user_ip)
        logger.info("User IP in Middleware", user_ip=user_ip)
        try:
            response = await call_next(request)
        finally:
            structlog.contextvars.clear_contextvars()
        return response

# ミドルウェアの追加
app.add_middleware(AddUserIPMiddleware)

# インポートしたルーターをアプリケーションに追加
app.include_router(router)

# このスクリプトが直接実行された場合、Uvicornサーバーを起動
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
