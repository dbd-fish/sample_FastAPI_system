import os
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError

from app.core.http_exception_handler import http_exception_handler
from app.core.log_config import logger
from app.core.request_validation_error import validation_exception_handler
from app.database import database
from app.middleware import AddUserIPMiddleware, ErrorHandlerMiddleware
from app.routes import router

# タイムゾーンをJST（日本標準時）に設定
os.environ['TZ'] = 'Asia/Tokyo'
time.tzset()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    アプリケーションのライフサイクル管理を行うコンテキストマネージャ。
    """
    logger.info("Application startup - connecting to database.")

    # 明示的にイベントループを設定（最新バージョンでも安全）
    # loop = asyncio.get_running_loop()
    # asyncio.set_event_loop(loop)

    await database.connect()
    yield
    logger.info("Application shutdown - disconnecting from database.")
    await database.disconnect()

# FastAPIアプリケーションのインスタンスを作成し、lifespanを設定
app = FastAPI(lifespan=lifespan)

# ミドルウェアの追加 (ユーザーIP記録とエラーハンドリング)
app.add_middleware(AddUserIPMiddleware)
app.add_middleware(ErrorHandlerMiddleware)

# 例外ハンドラの登録
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)

# ルーターをアプリケーションに追加
app.include_router(router)

# このスクリプトが直接実行された場合、Uvicornサーバーを起動
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
