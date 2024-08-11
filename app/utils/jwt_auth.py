from datetime import timedelta, datetime
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.model.model import User as UserModel
from jose import jwt, JWTError
from passlib.context import CryptContext
from dotenv import load_dotenv
import os


load_dotenv()

secret_key = os.getenv("SECRET_KEY")
expire_min = os.getenv("EXPIRE_MINUTES")
algorithum = os.getenv("ALGORITHUM")

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")
bcrypt_context = CryptContext(schemes=["bcrypt"])

# Create token
async def create_access_token(id: int, username: str):
    encode = {"sub": username, "id": id}
    expires = datetime.utcnow() + timedelta(minutes=int(expire_min))
    encode.update({"exp": expires})
    return jwt.encode(encode, secret_key, algorithm=algorithum)

# Get current user from token
async def get_current_user(db: Session, token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithum])
        username: str = payload.get("sub")
        id: int = payload.get("id")
        expires: datetime = payload.get("exp")
        if datetime.fromtimestamp(expires) < datetime.utcnow():
            return None
        if username is None or id is None:
            return None
        db_user = db.query(UserModel).filter(UserModel.id == id).first()
        return db_user
    except JWTError:
        return None

# Authenticate
async def authenticate(db: Session, username: str, password: str):
    db_user = db.query(UserModel).filter(UserModel.username == username).first()
    if not db_user:
        return None
    if not bcrypt_context.verify(password, db_user.hashed_password):
        return None
    return db_user