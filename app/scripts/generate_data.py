import asyncio
import random
from datetime import date, datetime, timedelta

from sqlalchemy import insert, select, func

from app.database.database import AsyncSessionLocal
from app.models.employee import Employee
from app.models.request import Request
from app.models.enums import RequestStatus


EMPLOYEES_COUNT = 1000
REQUESTS_COUNT = 1000000
BATCH_SIZE = 20000


DEPARTMENTS = [
    "IT",
    "HR",
    "Accounting",
    "Sales",
    "Production",
]

POSITIONS = [
    "Engineer",
    "Manager",
    "Analyst",
    "Specialist",
    "Technician",
]


async def generate_employees():

    async with AsyncSessionLocal() as db:

        result = await db.execute(
            select(func.count(Employee.id))
        )

        employees_count = result.scalar()

        if employees_count > 0:
            print(
                f"Employees already exist ({employees_count}). Skipping..."
            )
            return

        employees = [
            {
                "full_name": f"Employee {i}",
                "department": random.choice(DEPARTMENTS),
                "position": random.choice(POSITIONS),
            }
            for i in range(1, EMPLOYEES_COUNT + 1)
        ]

        await db.execute(
            insert(Employee),
            employees
        )

        await db.commit()

        print(f"Created {EMPLOYEES_COUNT} employees.")


async def generate_requests():

    async with AsyncSessionLocal() as db:

        result = await db.execute(
            select(func.max(Request.number))
        )

        start_number = result.scalar() or 0

        print(f"Starting request numbering from {start_number + 1}")

        for start in range(0, REQUESTS_COUNT, BATCH_SIZE):

            end = min(
                start + BATCH_SIZE,
                REQUESTS_COUNT
            )

            batch = []

            for i in range(start, end):

                batch.append(
                    {
                        "number": start_number + i + 1,
                        "created_at": datetime.now(),
                        "author_id": random.randint(
                            1,
                            EMPLOYEES_COUNT
                        ),
                        "executor_id": random.randint(
                            1,
                            EMPLOYEES_COUNT
                        ),
                        "description": f"Request #{start_number + i + 1}",
                        "deadline": date.today()
                        + timedelta(
                            days=random.randint(-30, 30)
                        ),
                        "status": random.choice(
                            list(RequestStatus)
                        ),
                    }
                )

            await db.execute(
                insert(Request),
                batch
            )

            await db.commit()

            print(
                f"Inserted {end}/{REQUESTS_COUNT} requests"
            )

        print("Generation completed successfully.")


async def main():

    print("=== Test data generation ===")

    await generate_employees()
    await generate_requests()

    print("Done.")


if __name__ == "__main__":
    asyncio.run(main())