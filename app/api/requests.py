from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.schemas.request import RequestCreate, RequestResponse, RequestStatusUpdate
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

    return await RequestService.create_request(
        db=db,
        request_data=request
    )


@router.get(
    "",
    response_model=list[RequestResponse]
)
async def get_requests(
    db: AsyncSession = Depends(get_db)
):

    requests = await RequestService.get_requests(db)

    return [
        RequestResponse(
            id=req.id,
            number=req.number,
            created_at=req.created_at,
            description=req.description,
            deadline=req.deadline,
            status=req.status,
            author=req.author.full_name,
            executor=req.executor.full_name,
        )
        for req in requests
    ]

@router.patch("/{request_id}/status")
async def update_request_status(
    request_id: int,
    data: RequestStatusUpdate,
    db: AsyncSession = Depends(get_db)
):

    return await RequestService.update_status(
        db=db,
        request_id=request_id,
        new_status=data.status
    )