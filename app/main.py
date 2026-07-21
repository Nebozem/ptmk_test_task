from fastapi import FastAPI

import app.models

from app.api.employees import router as employee_router
from app.api.requests import router as request_router
from app.api.reports import router as report_router


app = FastAPI(
    title="PTMK Test Task",
    description="Employee request tracking system",
    version="1.0.0"
)

app.include_router(employee_router)
app.include_router(request_router)
app.include_router(report_router)


@app.get("/")
def root():
    return {"message": "Application is running"}