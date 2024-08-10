from fastapi import FastAPI, APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from app.databse.database import get_db
from app.schemas.schemas import UserCreate
from app.service import service
from app.databse.database import Base, engine

app = FastAPI()
router = APIRouter(prefix="/users", tags=["Users"])

# Create all tables
Base.metadata.create_all(bind=engine)


@app.get("/api/healthchecker")
def root():
    return {"message": "Welcome to FastAPI with SQLAlchemy"}


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends (get_db)):
    db_user = await service.existing_user(db, user.username, user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="username or email already in use",
        )
    db_user = await service.create_user(db, user)
    access_token = await service.create_access_token (db_user.id, db_user.username)

    return {
        "access_token": access_token,
        "token_type":"bearer",
        "username": db_user.username,
    }

app.include_router(router)