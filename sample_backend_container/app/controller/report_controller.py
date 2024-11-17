from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.report import Report  # SQLAlchemy モデル
from app.schema.report import RequestReport, ResponseReport  # Pydantic モデル
from app.services.report_service import create_report, update_report, delete_report, get_report_by_id_service

router = APIRouter()

# 新規作成のエンドポイント
@router.post("/reports", response_model=ResponseReport)
async def create_report_endpoint(report: RequestReport, db: AsyncSession = Depends(get_db)):
    """
    新しいレポートを作成するエンドポイント。

    :param report: 作成するレポートのデータ
    :param db: データベースセッション (依存関係として注入)
    :return: 作成されたレポートのオブジェクト
    """
    # リクエストデータを SQLAlchemy モデルに変換して保存
    new_report = Report(
        user_id="user-uuid",
        title="Sample Report",
        content="Sample content",
        format=1,
        visibility=3
    )
    db.add(new_report)
    await db.commit()
    await db.refresh(new_report)
    return new_report

# 更新のエンドポイント
@router.put("/reports/{report_id}", response_model=ResponseReport)
async def update_report_endpoint(report_id: str, updated_report: RequestReport, db: AsyncSession = Depends(get_db)):
    """
    指定されたIDのレポートを更新するエンドポイント。

    :param report_id: 更新対象のレポートID
    :param updated_report: 更新するデータ
    :param db: データベースセッション (依存関係として注入)
    :return: 更新されたレポートのオブジェクト
    """
    # レポートの取得と更新
    report = await db.get(Report, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    for key, value in updated_report.dict(exclude_unset=True).items():
        setattr(report, key, value)
    
    await db.commit()
    await db.refresh(report)
    return report

# 削除のエンドポイント
@router.delete("/reports/{report_id}")
async def delete_report_endpoint(report_id: str, db: AsyncSession = Depends(get_db)):
    """
    指定されたIDのレポートを削除するエンドポイント。

    :param report_id: 削除対象のレポートID
    :param db: データベースセッション (依存関係として注入)
    :return: 削除成功メッセージ
    """
    # レポートの取得と削除
    report = await db.get(Report, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    await db.delete(report)
    await db.commit()
    return {"message": "Report deleted successfully"}

# 特定IDのレポート取得エンドポイント
@router.get("/reports/{report_id}", response_model=ResponseReport)
async def get_report_by_id(report_id: str, db: AsyncSession = Depends(get_db)):
    """
    指定されたIDのレポートを取得するエンドポイント。

    :param report_id: 取得対象のレポートID
    :param db: データベースセッション (依存関係として注入)
    :return: 指定されたIDのレポート
    """
    # レポートの取得
    report = await db.get(Report, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report
