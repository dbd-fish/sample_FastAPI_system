from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schema.report import RequestReport, ResponseReport
from app.services.report_service import create_report, update_report, delete_report, get_report_by_id_service

router = APIRouter()

@router.post("/reports", response_model=ResponseReport)
async def create_report_endpoint(report: RequestReport, db: AsyncSession = Depends(get_db)):
    return await create_report(report, db)

@router.put("/reports/{report_id}", response_model=ResponseReport)
async def update_report_endpoint(report_id: str, updated_report: RequestReport, db: AsyncSession = Depends(get_db)):
    return await update_report(report_id, updated_report, db)

@router.delete("/reports/{report_id}")
async def delete_report_endpoint(report_id: str, db: AsyncSession = Depends(get_db)):
    await delete_report(report_id, db)
    return {"message": "Report deleted successfully"}

@router.get("/reports/{report_id}", response_model=ResponseReport)
async def get_report_by_id(report_id: str, db: AsyncSession = Depends(get_db)):
    return await get_report_by_id_service(report_id, db)
