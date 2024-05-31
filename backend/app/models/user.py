from sqlalchemy import Integer, String, DateTime, func
from sqlalchemy.orm import relationship, mapped_column


from app.database.core import Base

class User(Base):
    __tablename__ = "user"

    id = mapped_column(Integer, primary_key=True)
    email = mapped_column(String, unique=True, index=True)
    hashed_password = mapped_column(String)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column(DateTime(timezone=True), onupdate=func.now())
    files = relationship(
        "File",
        back_populates="owner",
    )
