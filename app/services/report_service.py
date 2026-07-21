from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.request import Request
from app.models.employee import Employee
from app.models.enums import RequestStatus


class ReportService:

    @staticmethod
    async def get_report(
        db: AsyncSession
    ):

        total_requests = await db.scalar(
            select(func.count())
            .select_from(Request)
        )

        total_employees = await db.scalar(
            select(func.count())
            .select_from(Employee)
        )

        new_requests = await db.scalar(
            select(func.count())
            .select_from(Request)
            .where(
                Request.status == RequestStatus.NEW
            )
        )

        in_progress_requests = await db.scalar(
            select(func.count())
            .select_from(Request)
            .where(
                Request.status == RequestStatus.IN_PROGRESS
            )
        )

        completed_requests = await db.scalar(
            select(func.count())
            .select_from(Request)
            .where(
                Request.status == RequestStatus.DONE
            )
        )

        return {
            "total_requests": total_requests,
            "total_employees": total_employees,
            "requests_by_status": {
                "new": new_requests,
                "in_progress": in_progress_requests,
                "completed": completed_requests
            }
        }