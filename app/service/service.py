from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.model.model import User as UserModel
from passlib.context import CryptContext
from sqlalchemy.exc import SQLAlchemyError

from app.schemas.schemas import UserCreate, UserUpdate


oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")
bcrypt_context = CryptContext(schemes=["bcrypt"])


# Check existing users with username and email
async def existing_user(db: Session, username: str, email: str):
    try:
        db_user = db.query(UserModel).filter(UserModel.username == username).first()
        if db_user:
            return db_user
        db_user = db.query(UserModel).filter(UserModel.email == email).first()
        if db_user:
            return db_user
        return None
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database query failed")


# Create user
async def create_user(db: Session, user: UserCreate):
    try:
        db_user = UserModel(
            username=user.username,
            email=user.email,
            hashed_password=bcrypt_context.hash(user.password),
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create user")


# Update user
async def update_user(db: Session, db_user: UserModel, user_update: UserUpdate):
    try:
        if user_update.username is not None:
            db_user.username = user_update.username
        if user_update.email is not None:
            db_user.email = user_update.email
        if user_update.password is not None:
            db_user.hashed_password = bcrypt_context.hash(user_update.password)

        db.commit()
        db.refresh(db_user)
        return db_user
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update user")


# Delete user
async def delete_user(db: Session, db_user: UserModel):
    try:
        db.delete(db_user)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete user")
