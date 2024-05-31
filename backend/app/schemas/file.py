from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class FileBase(BaseModel):
    path: str
    is_folder: bool = False
    created_at: datetime | None = None
    updated_at: datetime | None = None

class FileCreate(BaseModel):
    path: str

class FileUpdate(BaseModel):
    path: Optional[str] = None

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
