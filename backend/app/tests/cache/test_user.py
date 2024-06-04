from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.cache.core import redis_db as redis
from app.tests.utils.user import create_random_user

def test_write_user_to_cache(session: Session) -> None:
    user = create_random_user(session=session)

    assert user

    redis.write_user_to_cache(user.id, user.email, jsonable_encoder(user))

    assert redis.exists(f"user:{user.id}") == 1
    assert redis.exists(f"email:{user.email}") == 1

def test_read_user_by_id_from_cache(session: Session) -> None:
    user = create_random_user(session=session)

    assert user

    redis.write_user_to_cache(user.id, user.email, jsonable_encoder(user))

    user_obj = redis.read_user_by_id_from_cache(user.id)

    assert user_obj
    assert user_obj["id"] == user.id
    assert user_obj["email"] == user.email

def test_read_user_by_email_from_cache(session: Session) -> None:
    user = create_random_user(session=session)

    assert user

    redis.write_user_to_cache(user.id, user.email, jsonable_encoder(user))

    user_obj = redis.read_user_by_email_from_cache(user.email)

    assert user_obj
    assert user_obj["id"] == user.id
    assert user_obj["email"] == user.email

def test_delete_user_from_cache(session: Session) -> None:
    user = create_random_user(session=session)

    assert user

    redis.write_user_to_cache(user.id, user.email, jsonable_encoder(user))

    redis.delete_user_from_cache(user.id)

    assert redis.exists(f"user:{user.id}") == 0
    assert redis.exists(f"email:{user.email}") == 0

    user_obj = redis.read_user_by_id_from_cache(user.id)

    assert not user_obj
