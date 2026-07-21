from fastapi import HTTPException

from datetime import date

from sqlalchemy import select, and_
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
            status=RequestStatus.NEW
        )

        db.add(request)

        await db.commit()
        await db.refresh(request)

        # Загружаем связи для response_model
        result = await db.execute(
            select(Request)
            .options(
                joinedload(Request.author),
                joinedload(Request.executor)
            )
            .where(Request.id == request.id)
        )

        return result.scalar_one()


    @staticmethod
    async def get_requests(
        db: AsyncSession,
        status: RequestStatus | None = None,
        executor_id: int | None = None,
        department: str | None = None,
        overdue: bool = False,
        limit: int = 20,
        offset: int = 0
    ) -> list[Request]:

        query = (
            select(Request)
            .options(
                joinedload(Request.author),
                joinedload(Request.executor)
            )
            .order_by(Request.id)
        )


        filters = []


        if status:
            filters.append(
                Request.status == status
            )


        if executor_id:
            filters.append(
                Request.executor_id == executor_id
            )


        if department:

            query = query.join(
                Request.executor
            )

            filters.append(
                Employee.department == department
            )


        if overdue:

            filters.append(
                Request.deadline < date.today()
            )


        if filters:
            query = query.where(
                and_(*filters)
            )


        query = (
            query
            .offset(offset)
            .limit(limit)
        )


        result = await db.execute(query)

        return result.unique().scalars().all()



    @staticmethod
    async def update_status(
        db: AsyncSession,
        request_id: int,
        new_status: RequestStatus
    ) -> Request:

        result = await db.execute(
            select(Request)
            .options(
                joinedload(Request.author),
                joinedload(Request.executor)
            )
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


        result = await db.execute(
            select(Request)
            .options(
                joinedload(Request.author),
                joinedload(Request.executor)
            )
            .where(Request.id == request.id)
        )

        return result.scalar_one()



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


        result = await db.execute(
            select(Request)
            .options(
                joinedload(Request.author),
                joinedload(Request.executor)
            )
            .where(Request.id == request.id)
        )

        return result.scalar_one()