from datetime import timedelta, datetime

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.model.model import User as UserModel
from jose import jwt, JWTError
from passlib.context import CryptContext

from app.schemas.schemas import UserCreate

SECRET_KEY = "mysecretkey"
EXPIRE_MINUTES = 60 * 20
ALGORITHUM = "HS256"

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
    expires= datetime.utcnow() + timedelta (minutes=EXPIRE_MINUTES)
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHUM)


# get current user from token
async def get_current_user(db: Session, token: str = Depends (oauth2_bearer)):
    try:
        payload=jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHUM])
        username: str = payload.get("sub")
        id: int = payload.get("id")
        expires: datetime = payload.get("exp")
        if expires < datetime.utcnow():
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
