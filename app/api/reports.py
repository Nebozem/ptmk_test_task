from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.services.report_service import ReportService

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.get("")
async def get_report(
    db: AsyncSession = Depends(get_db)
):
    return await ReportService.get_report(db)