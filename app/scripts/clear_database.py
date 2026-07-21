import asyncio

from sqlalchemy import select, func, text

from app.database.database import AsyncSessionLocal
from app.models.employee import Employee
from app.models.request import Request


async def clear_database():

    async with AsyncSessionLocal() as db:

        employees_count = await db.scalar(
            select(func.count(Employee.id))
        )

        requests_count = await db.scalar(
            select(func.count(Request.id))
        )

        print("=== Database cleanup ===")
        print(f"Employees: {employees_count}")
        print(f"Requests : {requests_count}")

        if employees_count == 0 and requests_count == 0:
            print("\nDatabase is already empty.")
            return

        await db.execute(
            text("TRUNCATE TABLE requests RESTART IDENTITY CASCADE;")
        )

        await db.execute(
            text("TRUNCATE TABLE employees RESTART IDENTITY CASCADE;")
        )

        await db.commit()

        print("\nCleanup completed successfully.")
        print(f"Deleted employees: {employees_count}")
        print(f"Deleted requests : {requests_count}")


async def main():
    await clear_database()


if __name__ == "__main__":
    asyncio.run(main())