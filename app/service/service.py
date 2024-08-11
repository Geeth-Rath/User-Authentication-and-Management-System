from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.model.model import User as UserModel
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

from app.schemas.schemas import UserCreate, UserUpdate

load_dotenv()

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")
bcrypt_context = CryptContext(schemes=["bcrypt"])

# Check existing users with username and email
async def existing_user(db: Session, username: str, email: str):
    db_user = db.query(UserModel).filter(UserModel.username == username).first()
    if db_user:
        return db_user
    db_user = db.query(UserModel).filter(UserModel.email == email).first()
    if db_user:
        return db_user
    return None

# Create user
async def create_user(db: Session, user: UserCreate):
    db_user = UserModel(
        username=user.username,
        email=user.email,
        hashed_password=bcrypt_context.hash(user.password),
    )
    db.add(db_user)
    db.commit()
    return db_user

# Update user
async def update_user(db: Session, db_user: UserModel, user_update: UserUpdate):
    if user_update.username is not None:
        db_user.username = user_update.username
    if user_update.email is not None:
        db_user.email = user_update.email
    if user_update.password is not None:
        db_user.hashed_password = bcrypt_context.hash(user_update.password)

    db.commit()
    db.refresh(db_user)
    return db_user

# Delete user
async def delete_user(db: Session, db_user: UserModel):
    db.delete(db_user)
    db.commit()
