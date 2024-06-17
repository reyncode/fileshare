from sqlalchemy import ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship, mapped_column

from app.database.base import Base

class File(Base):
    __tablename__ = "file"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String)
    access_key = mapped_column(String, unique=True)
    size = mapped_column(Integer, default=0)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column(DateTime(timezone=True), onupdate=func.now())
    owner_id = mapped_column(Integer, ForeignKey("user.id"))
    owner = relationship(
        "User",
        back_populates="files",
    )
