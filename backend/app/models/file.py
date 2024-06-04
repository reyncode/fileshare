from sqlalchemy import Boolean, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship, mapped_column

from app.database.base import Base

class File(Base):
    __tablename__ = "file"

    id = mapped_column(Integer, primary_key=True)
    path = mapped_column(String, index=True)
    is_folder = mapped_column(Boolean, default=False)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column(DateTime(timezone=True), onupdate=func.now())
    owner_id = mapped_column(Integer, ForeignKey("user.id"))
    owner = relationship(
        "User",
        back_populates="files",
    )
