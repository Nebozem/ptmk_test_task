from datetime import date, datetime

from pydantic import BaseModel

from app.models.enums import RequestStatus


class RequestCreate(BaseModel):
    number: int
    author_id: int
    executor_id: int
    description: str
    deadline: date


class RequestResponse(BaseModel):
    id: int
    number: int
    created_at: datetime

    description: str
    deadline: date
    status: RequestStatus

    author: str
    executor: str

    model_config = {
        "from_attributes": True
    }

class RequestStatusUpdate(BaseModel):
    status: RequestStatus

class ExecutorUpdate(BaseModel):
    executor_id: int