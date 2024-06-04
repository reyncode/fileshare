from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

import app.database.base as model_base

from app.crud.user import user_crud
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.config import settings

engine = create_engine(
    str(settings.SQLALCHEMY_TESTING_DATABASE_URI),
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)

model_base.Base.metadata.create_all(bind=engine)

def init_db(session: Session) -> None:

    user = session.scalars(
        select(User).filter_by(email=settings.TEST_USER_EMAIL)
    ).first()

    if not user:
        user_in = UserCreate(
            email=settings.TEST_USER_EMAIL, 
            password=settings.TEST_USER_PASSWORD
        )
        user = user_crud.create_user(session=session, user_create=user_in)

