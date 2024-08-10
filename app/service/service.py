from datetime import timedelta, datetime

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.model.model import User as UserModel
from jose import jwt, JWTError
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

from app.schemas.schemas import UserCreate, UserUpdate

load_dotenv()

secret_key = os.getenv("SECRET_KEY")
expire_min = int(os.getenv("EXPIRE_MINUTES"))
algorithum = os.getenv("ALGORITHUM")


oauth2_bearer = OAuth2PasswordBearer(tokenUrl = "token")
bcrypt_context = CryptContext(schemes = ["bcrypt"])

# check existing users with username and email
async def existing_user(db: Session, username: str, email:str):
    db_user = db.query(UserModel).filter(UserModel.username == username).first()
    if db_user:
        return db_user
    db_user = db.query(UserModel).filter(UserModel.email == email).first()
    if db_user:
        return db_user
    return None


# create token
#jwt = {encoded data, secret key, algorithm}
async def create_access_token (id: int, username: str):
    encode = {"sub": username, "id": id}
    expires= datetime.utcnow() + timedelta (minutes=expire_min)
    encode.update({"exp": expires})
    return jwt.encode(encode, secret_key, algorithm=algorithum)


# get current user from token
async def get_current_user(db: Session, token: str = Depends (oauth2_bearer)):
    try:
        payload=jwt.decode(token, secret_key, algorithms=[algorithum])
        username: str = payload.get("sub")
        id: int = payload.get("id")
        expires: datetime = payload.get("exp")
        # if expires < datetime.utcnow():
        #     return None
        if datetime.fromtimestamp(expires) < datetime.utcnow():
            return None
        if username is None or id is None:
            return None
        db_user = db.query(UserModel).filter(UserModel.id == id).first()
        return db_user
    except JWTError:
        return None

#create user
async def create_user(db: Session, user: UserCreate):
    db_user = UserModel(
            username=user.username,
            email=user.email,
            hashed_password=bcrypt_context.hash(user.password),
    )
    db.add(db_user)
    db.commit()
    return db_user


#authenticate
async def authenticate(db: Session, username: str, password: str):
    db_user = db.query(UserModel).filter(UserModel.username == username).first()
    if not db_user:
        return None
    if not bcrypt_context.verify(password, db_user.hashed_password):
        return None
    return db_user


# update user

async def update_user(db: Session, db_user: UserModel, user_update: UserUpdate):
    if user_update.username:
        db_user.username = user_update.username
    if user_update.email:
        db_user.email = user_update.email
    if user_update.password:
        db_user.hashed_password = bcrypt_context.hash(user_update.password)

    db.commit()
    db.refresh(db_user)

    return db_user

# delete user
async def delete_user(db: Session, db_user: UserModel):
    db.delete(db_user)
    db.commit()
