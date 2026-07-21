import asyncio
import argparse

from sqlalchemy import select, func
from sqlalchemy.orm import joinedload

from app.database.database import AsyncSessionLocal
from app.models.employee import Employee
from app.models.request import Request


async def show_employees(limit: int, offset: int):

    async with AsyncSessionLocal() as db:

        total = await db.scalar(
            select(func.count()).select_from(Employee)
        )

        print(f"\nTotal employees: {total}")

        result = await db.execute(
            select(Employee)
            .order_by(Employee.id)
            .offset(offset)
            .limit(limit)
        )

        employees = result.scalars().all()

        if not employees:
            print("Employees not found.")
            return

        print(f"\n=== Employees ({len(employees)}) ===")
        print(f"Offset: {offset}, Limit: {limit}\n")

        for employee in employees:
            print(
                f"[{employee.id}] "
                f"{employee.full_name} | "
                f"{employee.department} | "
                f"{employee.position}"
            )


async def show_requests(limit: int, offset: int):

    async with AsyncSessionLocal() as db:

        total = await db.scalar(
            select(func.count()).select_from(Request)
        )

        print(f"\nTotal requests: {total}")

        result = await db.execute(
            select(Request)
            .options(
                joinedload(Request.author),
                joinedload(Request.executor)
            )
            .order_by(Request.id)
            .offset(offset)
            .limit(limit)
        )

        requests = result.scalars().all()

        if not requests:
            print("Requests not found.")
            return

        print(f"\n=== Requests ({len(requests)}) ===")
        print(f"Offset: {offset}, Limit: {limit}\n")

        for request in requests:

            print(
                f"[{request.id}] "
                f"№{request.number} | "
                f"{request.status.value} | "
                f"Author: {request.author.full_name} | "
                f"Executor: {request.executor.full_name} | "
                f"Deadline: {request.deadline}"
            )


async def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--table",
        choices=["employees", "requests"],
        required=True
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=20
    )

    parser.add_argument(
        "--offset",
        type=int,
        default=0
    )

    args = parser.parse_args()

    if args.table == "employees":
        await show_employees(
            args.limit,
            args.offset
        )

    else:
        await show_requests(
            args.limit,
            args.offset
        )


if __name__ == "__main__":
    asyncio.run(main())