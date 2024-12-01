from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from app.database import database, get_db
from app.routes import router
from app.core.log_config import logger
from contextlib import asynccontextmanager
from app.middleware import AddUserIPMiddleware, ErrorHandlerMiddleware
import os
import time
from app.core.request_validation_error import validation_exception_handler


# タイムゾーンをJST（日本標準時）に設定
os.environ['TZ'] = 'Asia/Tokyo'
time.tzset()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    アプリケーションのライフサイクル管理を行うコンテキストマネージャ。
    """
    logger.info("Application startup - connecting to database.")
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

# ルーターをアプリケーションに追加
app.include_router(router)

# このスクリプトが直接実行された場合、Uvicornサーバーを起動
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
