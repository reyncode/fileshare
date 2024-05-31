from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

from app.schemas.file import File

class UserBase(BaseModel):
    email: EmailStr
    created_at: datetime | None = None
    updated_at: datetime | None = None

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None

class UpdatePassword(BaseModel):
    current_password: str
    new_password: str

class User(UserBase):
    id: int
    hashed_password: str
    files: list[File] = []

    class Config:
        from_attributes = True

class UserPublic(UserBase):
    id: int
