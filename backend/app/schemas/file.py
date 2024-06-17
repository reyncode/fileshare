from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class FileBase(BaseModel):
    name: str
    access_key: str
    size: int
    created_at: datetime | None = None
    updated_at: datetime | None = None

class FileCreate(BaseModel):
    name: str
    access_key: str
    size: Optional[int] = 0

class FileUpdate(BaseModel):
    name: Optional[str] = None
    access_key: Optional[str] = None
    size: Optional[int] = 0

class File(FileBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True

class FilePublic(FileBase):
    id: int
    owner_id: int

class FilesPublic(BaseModel):
    data: list[FilePublic]
    count: int
