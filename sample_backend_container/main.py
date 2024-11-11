from fastapi import FastAPI
from app.database import database
from app.routes import router
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # アプリケーション起動時の処理
    await database.connect()
    yield
    # アプリケーション終了時の処理
    await database.disconnect()

# FastAPIアプリケーションインスタンスを作成し、lifespanを設定
app = FastAPI(lifespan=lifespan)

# インポートしたルーターをアプリケーションに追加
app.include_router(router)

# このスクリプトが直接実行された場合、Uvicornサーバーを起動
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
