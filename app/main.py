from fastapi import FastAPI, APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.databse.database import get_db
from app.schemas.schemas import UserCreate, UserResponse, UserUpdate
from app.service import service
from app.utils import jwt_auth
from app.databse.database import Base, engine


app = FastAPI()
router = APIRouter(prefix="/users", tags=["Users"])

Base.metadata.create_all(bind=engine)

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends (get_db)):
    db_user = await service.existing_user(db, user.username, user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="username or email already in use",
        )
    db_user = await service.create_user(db, user)
    access_token = await jwt_auth.create_access_token (db_user.id, db_user.username)

    return {
        "access_token": access_token,
        "token_type":"bearer",
        "username": db_user.username,
    }


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db:Session = Depends (get_db)
):
    db_user = await jwt_auth.authenticate(db, form_data.username, form_data.password)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="incorrect username or password",
        )
    access_token = await jwt_auth.create_access_token (db_user.id, db_user.username)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
async def get_current_user(token: str, db: Session = Depends (get_db)):
    db_user = await jwt_auth.get_current_user(db, token)
    if not db_user:
        raise HTTPException (status_code=status.HTTP_401_UNAUTHORIZED, detail="you are not authenticated")

    return db_user

@router.put("/me", status_code=status.HTTP_200_OK)
async def update_user(
        token: str,
        user: UserUpdate,
        db: Session = Depends(get_db)
):
    db_user = await jwt_auth.get_current_user(db, token)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update this user",
        )
    updated_user = await service.update_user(db, db_user, user)

    return {"message": "User updated successfully"}

@router.delete("/me", status_code=status.HTTP_200_OK)
async def delete_user(token: str, db: Session = Depends(get_db)):
    db_user = await jwt_auth.get_current_user(db, token)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete this user",
        )
    await service.delete_user(db, db_user)
    return {"message": "User deleted successfully"}

app.include_router(router)