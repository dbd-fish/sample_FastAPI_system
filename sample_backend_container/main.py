from fastapi import FastAPI  # FastAPIフレームワークをインポート
from app.database import database  # データベース接続オブジェクトをインポート
from app.routes import router  # アプリケーションのルーティングをインポート

# FastAPIアプリケーションインスタンスを作成
app = FastAPI()

# アプリケーションが起動する際に呼び出されるイベントハンドラ
@app.on_event("startup")
async def startup():
    # データベースに接続
    await database.connect()

# アプリケーションがシャットダウンする際に呼び出されるイベントハンドラ
@app.on_event("shutdown")
async def shutdown():
    # データベース接続を切断
    await database.disconnect()

# インポートしたルーターをアプリケーションに追加
app.include_router(router)

# このスクリプトが直接実行された場合、Uvicornサーバーを起動
if __name__ == "__main__":
    import uvicorn  # Uvicornサーバーをインポート
    # UvicornでFastAPIアプリケーションを起動
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    # "main:app" は "main.py" の "app" インスタンスを指定している
    # host="0.0.0.0" は全てのネットワークインターフェイスでリッスン
    # port=8000 は8000番ポートで起動
    # reload=True はコード変更時に自動で再起動するように設定（開発モード用）
