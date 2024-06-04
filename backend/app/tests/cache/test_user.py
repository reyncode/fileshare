from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.cache.core import client
from app.cache.user import user_cache
from app.tests.utils.user import create_random_user

def test_write_user_to_cache(session: Session) -> None:
    user = create_random_user(session=session)

    assert user

    user_cache.write_user_to_cache(user.id, user.email, jsonable_encoder(user))

    assert client.exists(f"user:{user.id}") == 1
    assert client.exists(f"email:{user.email}") == 1

def test_read_user_by_id_from_cache(session: Session) -> None:
    user = create_random_user(session=session)

    assert user

    user_cache.write_user_to_cache(user.id, user.email, jsonable_encoder(user))

    user_obj = user_cache.read_user_by_id_from_cache(user.id)

    assert user_obj
    assert user_obj["id"] == user.id
    assert user_obj["email"] == user.email

def test_read_user_by_email_from_cache(session: Session) -> None:
    user = create_random_user(session=session)

    assert user

    user_cache.write_user_to_cache(user.id, user.email, jsonable_encoder(user))

    user_obj = user_cache.read_user_by_email_from_cache(user.email)

    assert user_obj
    assert user_obj["id"] == user.id
    assert user_obj["email"] == user.email

def test_delete_user_from_cache(session: Session) -> None:
    user = create_random_user(session=session)

    assert user

    user_cache.write_user_to_cache(user.id, user.email, jsonable_encoder(user))

    user_cache.delete_user_from_cache(user.id)

    assert client.exists(f"user:{user.id}") == 0
    assert client.exists(f"email:{user.email}") == 0

    user_obj = user_cache.read_user_by_id_from_cache(user.id)

    assert not user_obj
