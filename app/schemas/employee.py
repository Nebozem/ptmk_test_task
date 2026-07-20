from pydantic import BaseModel


class EmployeeCreate(BaseModel):
    full_name: str
    department: str
    position: str


class EmployeeResponse(BaseModel):
    id: int
    full_name: str
    department: str
    position: str

    model_config = {
        "from_attributes": True
    }