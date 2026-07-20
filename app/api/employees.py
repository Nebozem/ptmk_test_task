from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.services.employee_service import EmployeeService
from app.schemas.employee import EmployeeCreate, EmployeeResponse


router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)


@router.post(
    "",
    response_model=EmployeeResponse,
    status_code=201
)
async def create_employee(
    employee: EmployeeCreate,
    db: AsyncSession = Depends(get_db)
):

    return await EmployeeService.create_employee(
        db=db,
        employee_data=employee
    )


@router.get(
    "",
    response_model=list[EmployeeResponse]
)
async def get_employees(
    db: AsyncSession = Depends(get_db)
):

    return await EmployeeService.get_employees(db)