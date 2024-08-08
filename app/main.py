from fastapi import FastAPI, APIRouter, status

app = FastAPI()
router = APIRouter()


@app.get("/api/healthchecker")
def root():
    return {"message": "Welcome to FastAPI with SQLAlchemy"}

