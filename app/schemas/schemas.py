from pydantic import BaseModel, EmailStr, constr, field_validator
from datetime import datetime
import re


class UserBase(BaseModel):
    username: constr(min_length=3)
    email: EmailStr


class UserCreate(UserBase):
    password: str

    @field_validator('password')
    def validate_password(cls, value):
        pattern = r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$'

        if not re.match(pattern, value):
            raise ValueError(
                "Password must be at least 8 characters long, contain at least one uppercase letter, one lowercase letter, one digit, and one special character."
            )
        return value


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    hashed_password: str
    createdAt: datetime

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    username: constr(min_length=3) | None = None
    email: EmailStr | None = None
    password: str | None = None

    @field_validator('password', mode='before')
    def validate_password(cls, value):
        if value is None:
            return value

        pattern = r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$'

        if not re.match(pattern, value):
            raise ValueError(
                "Password must be at least 8 characters long, contain at least one uppercase letter, one lowercase letter, one digit, and one special character."
            )
        return value
