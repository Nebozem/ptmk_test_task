from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.employee import Employee


class EmployeeService:

    @staticmethod
    async def create_employee(
        db: AsyncSession,
        employee_data
    ) -> Employee:

        employee = Employee(
            full_name=employee_data.full_name,
            department=employee_data.department,
            position=employee_data.position,
        )

        db.add(employee)

        await db.commit()
        await db.refresh(employee)

        return employee


    @staticmethod
    async def get_employees(
        db: AsyncSession
    ):

        result = await db.execute(
            select(Employee)
        )

        return result.scalars().all()