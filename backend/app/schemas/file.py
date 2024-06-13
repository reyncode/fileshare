from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class FileBase(BaseModel):
    name: str
    created_at: datetime | None = None
    updated_at: datetime | None = None

class FileCreate(BaseModel):
    name: str

class FileUpdate(BaseModel):
    name: Optional[str] = None

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
