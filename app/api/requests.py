from fastapi import APIRouter, Depends, Query, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.schemas.request import (
    RequestCreate,
    RequestResponse,
    RequestStatusUpdate,
    RequestStatus
)
from app.services.request_service import RequestService


router = APIRouter(
    prefix="/requests",
    tags=["Requests"]
)


@router.post(
    "",
    response_model=RequestResponse,
    status_code=201
)
async def create_request(
    request: RequestCreate,
    db: AsyncSession = Depends(get_db)
):

    created_request = await RequestService.create_request(
        db=db,
        request_data=request
    )

    return RequestResponse(
        id=created_request.id,
        number=created_request.number,
        created_at=created_request.created_at,
        description=created_request.description,
        deadline=created_request.deadline,
        status=created_request.status,
        author=created_request.author.full_name,
        executor=created_request.executor.full_name
    )


@router.get(
    "",
    response_model=list[RequestResponse]
)
async def get_requests(
    status: RequestStatus | None = None,
    executor_id: int | None = None,
    department: str | None = None,
    overdue: bool = False,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db)
):

    requests = await RequestService.get_requests(
        db=db,
        status=status,
        executor_id=executor_id,
        department=department,
        overdue=overdue,
        limit=limit,
        offset=offset
    )

    return [
        RequestResponse(
            id=request.id,
            number=request.number,
            created_at=request.created_at,
            description=request.description,
            deadline=request.deadline,
            status=request.status,
            author=request.author.full_name,
            executor=request.executor.full_name
        )
        for request in requests
    ]


@router.patch(
    "/{request_id}/status",
    response_model=RequestResponse
)
async def update_request_status(
    request_id: int,
    data: RequestStatusUpdate,
    db: AsyncSession = Depends(get_db)
):

    updated_request = await RequestService.update_status(
        db=db,
        request_id=request_id,
        new_status=data.status
    )

    if updated_request is None:
        raise HTTPException(
            status_code=404,
            detail="Request not found"
        )

    return RequestResponse(
        id=updated_request.id,
        number=updated_request.number,
        created_at=updated_request.created_at,
        description=updated_request.description,
        deadline=updated_request.deadline,
        status=updated_request.status,
        author=updated_request.author.full_name,
        executor=updated_request.executor.full_name
    )