from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import structlog

# ロガーの設定
logger = structlog.get_logger()

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    バリデーションエラーが発生した際のハンドラ。

    Args:
        request (Request): リクエストオブジェクト。
        exc (RequestValidationError): 発生したバリデーションエラー。

    Returns:
        JSONResponse: エラーレスポンス。
    """
    # エラーログの記録
    logger.error(
        "Request validation error occurred",
        errors=exc.errors(),
        body=exc.body,
        client_ip=request.client.host,
        url=request.url.path,
        method=request.method,
    )
    
    # JSONレスポンスを返却
    return JSONResponse(
        status_code=422,
        content={
            "detail": exc.errors(),
            "body": exc.body,
        },
    )
