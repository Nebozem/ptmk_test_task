from fastapi import FastAPI

app = FastAPI(
    title="PTMK Test Task",
    description="Employee request tracking system",
    version="1.0.0"
)


@app.get("/")
def root():
    return {"message": "Application is running"}