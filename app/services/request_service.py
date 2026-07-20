from fastapi import HTTPException

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.request import Request
from app.models.employee import Employee
from app.models.enums import RequestStatus
from app.schemas.request import RequestCreate


class RequestService:

    @staticmethod
    async def create_request(
        db: AsyncSession,
        request_data: RequestCreate
    ) -> Request:

        request = Request(
            number=request_data.number,
            author_id=request_data.author_id,
            executor_id=request_data.executor_id,
            description=request_data.description,
            deadline=request_data.deadline,
        )

        db.add(request)

        await db.commit()
        await db.refresh(request)

        return request


    @staticmethod
    async def get_requests(
        db: AsyncSession
    ) -> list[Request]:

        result = await db.execute(
            select(Request)
            .options(
                joinedload(Request.author),
                joinedload(Request.executor)
            )
        )

        return result.scalars().all()


    @staticmethod
    async def update_status(
        db: AsyncSession,
        request_id: int,
        new_status: RequestStatus
    ) -> Request:

        result = await db.execute(
            select(Request)
            .where(Request.id == request_id)
        )

        request = result.scalar_one_or_none()

        if not request:
            raise HTTPException(
                status_code=404,
                detail="Request not found"
            )


        allowed_transitions = {
            RequestStatus.NEW: [
                RequestStatus.IN_PROGRESS
            ],

            RequestStatus.IN_PROGRESS: [
                RequestStatus.DONE
            ],

            RequestStatus.DONE: []
        }


        if new_status not in allowed_transitions[request.status]:
            raise HTTPException(
                status_code=400,
                detail="Invalid status transition"
            )


        request.status = new_status

        await db.commit()
        await db.refresh(request)

        return request


    @staticmethod
    async def update_executor(
        db: AsyncSession,
        request_id: int,
        executor_id: int
    ) -> Request:

        request = await db.get(
            Request,
            request_id
        )

        if not request:
            raise HTTPException(
                status_code=404,
                detail="Request not found"
            )


        employee = await db.get(
            Employee,
            executor_id
        )

        if not employee:
            raise HTTPException(
                status_code=404,
                detail="Executor not found"
            )


        request.executor_id = executor_id

        await db.commit()
        await db.refresh(request)

        return request