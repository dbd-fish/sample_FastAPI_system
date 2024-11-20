from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schema.report import RequestReport, ResponseReport
from app.schema.user import UserResponse
from app.services.report_service import create_report, update_report, delete_report, get_report_by_id_service
from app.models.user import User  # 現在ログイン中のユーザーを表すモデル
from app.core.security import oauth2_scheme

router = APIRouter()

@router.post("/reports", response_model=ResponseReport)
async def create_report_endpoint(
    report: RequestReport,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(oauth2_scheme),
):
    """
    新しいレポートを作成するエンドポイント。

    Args:
        report (RequestReport): 作成するレポートのリクエストデータ。
        db (AsyncSession): データベースセッション。
        current_user (UserResponse): 現在ログイン中のユーザー。

    Returns:
        ResponseReport: 作成されたレポートのデータ。
    """
    # レポート作成ロジックを呼び出し
    endpoint_result = await create_report(report, db)
    return endpoint_result


@router.put("/reports/{report_id}", response_model=ResponseReport)
async def update_report_endpoint(
    report_id: str,
    updated_report: RequestReport,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(oauth2_scheme),
):
    """
    既存のレポートを更新するエンドポイント。

    Args:
        report_id (str): 更新するレポートのID。
        updated_report (RequestReport): 更新する内容を含むリクエストデータ。
        db (AsyncSession): データベースセッション。
        current_user (User): 現在ログイン中のユーザー。

    Returns:
        ResponseReport: 更新されたレポートのデータ。
    """
    # レポート更新ロジックを呼び出し
    endpoint_result = await update_report(report_id, updated_report, db)
    return endpoint_result


@router.delete("/reports/{report_id}")
async def delete_report_endpoint(
    report_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(oauth2_scheme),
):
    """
    指定されたレポートを削除するエンドポイント。

    Args:
        report_id (str): 削除するレポートのID。
        db (AsyncSession): データベースセッション。
        current_user (User): 現在ログイン中のユーザー。

    Returns:
        dict: 削除成功メッセージ。
    """
    # レポート削除ロジックを呼び出し
    endpoint_result = await delete_report(report_id, db)
    return endpoint_result


@router.get("/reports/{report_id}", response_model=ResponseReport)
async def get_report_by_id(
    report_id: str,
    db: AsyncSession = Depends(get_db),
):
    """
    指定されたIDのレポートを取得するエンドポイント。

    Args:
        report_id (str): 取得するレポートのID。
        db (AsyncSession): データベースセッション。

    Returns:
        ResponseReport: 取得したレポートのデータ。
    """
    # レポート取得ロジックを呼び出し
    endpoint_result = await get_report_by_id_service(report_id, db)
    return endpoint_result
