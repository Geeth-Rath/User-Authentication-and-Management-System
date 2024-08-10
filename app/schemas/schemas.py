from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    hashed_password:str
    createdAt: datetime

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
    password: str | None = None



