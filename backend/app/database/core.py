from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))

# TODO: check if this is being used anywhere; if not delete
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
