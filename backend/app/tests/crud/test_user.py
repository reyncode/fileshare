from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from app.core.security import verify_password

from app.crud.user import user_crud
from app.schemas.user import UserCreate, UserUpdate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_email, random_lower_string

def test_create_user(session: Session) -> None:
    email = random_email()
    password = random_lower_string(32)
    user_in = UserCreate(email=email, password=password)
    user = user_crud.create_user(session=session, user_create=user_in)

    assert user
    assert hasattr(user, "email")
    assert user.email == email
    assert hasattr(user, "hashed_password")
    assert hasattr(user, "created_at")
    assert hasattr(user, "updated_at")

def test_read_user(session: Session) -> None:
    user = create_random_user(session=session)

    assert user

    read_user = user_crud.read_user(session=session, id=user.id)

    assert read_user
    assert user.email == read_user.email
    assert jsonable_encoder(user) == jsonable_encoder(read_user)

def test_read_user_by_email(session: Session) -> None:
    user = create_random_user(session=session)

    assert user

    read_user = user_crud.read_user_by_email(session=session, email=user.email)

    assert read_user
    assert user.email == read_user.email
    assert jsonable_encoder(user) == jsonable_encoder(read_user)

def test_update_user(session: Session) -> None:
    user = create_random_user(session=session)

    assert user

    new_username = random_email()

    updated_user_in = UserUpdate(email=new_username)
    updated_user = user_crud.update_user(session=session, user_id=user.id, user_in=updated_user_in)

    assert updated_user
    assert updated_user.email == new_username

def test_update_user_password(session: Session) -> None:
    user = create_random_user(session=session)

    assert user

    new_password = random_lower_string(32)

    user_crud.update_user_password(session=session, user_id=user.id, password=new_password)
    updated_user = user_crud.read_user(session=session, id=user.id)

    assert updated_user
    assert verify_password(new_password, updated_user.hashed_password)

def test_delete_user(session: Session) -> None:
    user = create_random_user(session=session)

    assert user

    user_crud.delete_user(session=session, user_id=user.id)
    result = user_crud.read_user_by_email(session=session, email=user.email)

    assert result is None

def test_authenticate_user(session: Session) -> None:
    email = random_email()
    password = random_lower_string(32)
    user_in = UserCreate(email=email, password=password)
    user = user_crud.create_user(session=session, user_create=user_in)

    assert user

    authenticated_user = user_crud.authenticate(session=session, email=user.email, password=password)

    assert authenticated_user
    assert user.email == authenticated_user.email

def test_not_authenticate_user(session: Session) -> None:
    email = random_email()
    password = random_lower_string(32)

    user = user_crud.authenticate(session=session, email=email, password=password)

    assert user is None
