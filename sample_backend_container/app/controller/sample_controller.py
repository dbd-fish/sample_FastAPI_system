from fastapi import HTTPException


def sample_endpoint():
    # ビジネスロジックをサービス層で処理
    result = {"message": "Hello, World from Controller!"}
    return result
