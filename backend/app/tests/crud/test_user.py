from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from app.core.security import verify_password

from app.crud.user import users
from app.schemas.user import UserCreate, UserUpdate
from app.tests.utils.utils import random_email, random_lower_string

def test_create_user(session: Session) -> None:
    email = random_email()
    password = random_lower_string(32)
    user_in = UserCreate(email=email, password=password)
    user = users.create_user(session=session, user_create=user_in)

    assert user.email == email
    assert hasattr(user, "hashed_password")

def test_read_user(session: Session) -> None:
    password = random_lower_string(32)
    username = random_email()

    user_in = UserCreate(email=username, password=password)
    user = users.create_user(session=session, user_create=user_in)

    read_user = users.read_user(session=session, id=user.id)

    assert read_user
    assert user.email == read_user.email
    assert jsonable_encoder(user) == jsonable_encoder(read_user)

def test_read_user_by_email(session: Session) -> None:
    password = random_lower_string(32)
    username = random_email()

    user_in = UserCreate(email=username, password=password)
    user = users.create_user(session=session, user_create=user_in)

    read_user = users.read_user_by_email(session=session, email=user.email)

    assert read_user
    assert user.email == read_user.email
    assert jsonable_encoder(user) == jsonable_encoder(read_user)

def test_update_user(session: Session) -> None:
    password = random_lower_string(32)
    username = random_email()

    user_in = UserCreate(email=username, password=password)
    user = users.create_user(session=session, user_create=user_in)

    new_username = random_email()

    updated_user_in = UserUpdate(email=new_username)
    updated_user = users.update_user(session=session, db_user=user, user_in=updated_user_in)

    assert updated_user
    assert updated_user.email == new_username

def test_update_user_password(session: Session) -> None:
    password = random_lower_string(32)
    new_password = random_lower_string(32)
    username = random_email()

    user_in = UserCreate(email=username, password=password)
    user = users.create_user(session=session, user_create=user_in)

    users.update_user_password(session=session, db_user=user, password=new_password)
    updated_user = users.read_user(session=session, id=user.id)

    assert updated_user
    assert verify_password(new_password, updated_user.hashed_password)

def test_delete_user(session: Session) -> None:
    password = random_lower_string(32)
    username = random_email()

    user_in = UserCreate(email=username, password=password)
    user = users.create_user(session=session, user_create=user_in)

    users.delete_user(session=session, db_user=user)
    user = users.read_user_by_email(session=session, email=username)

    assert user is None

def test_authenticate_user(session: Session) -> None:
    email = random_email()
    password = random_lower_string(32)
    user_in = UserCreate(email=email, password=password)
    user = users.create_user(session=session, user_create=user_in)
    authenticated_user = users.authenticate(session=session, email=email, password=password)

    assert authenticated_user
    assert user.email == authenticated_user.email

def test_not_authenticate_user(session: Session) -> None:
    email = random_email()
    password = random_lower_string(32)
    user = users.authenticate(session=session, email=email, password=password)

    assert user is None
