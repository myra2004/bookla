from pydantic import BaseModel, EmailStr, Field

from datetime import datetime


class UserRegisterIn(BaseModel):
    email: EmailStr
    password: str = Field(max_length=16, min_length=6)


class UserRegisterOut(BaseModel):
    id: int
    email: EmailStr
    username: str | None = None
    created_at: datetime


class UserLoginOut(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str