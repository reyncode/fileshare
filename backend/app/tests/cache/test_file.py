from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.cache.core import redis_db as redis
from app.tests.utils.file import create_random_file
from app.tests.utils.user import create_random_user

def test_write_file_to_cache(session: Session) -> None:
    file = create_random_file(session=session)

    assert file

    redis.write_file_to_cache(file.id, file.owner_id, jsonable_encoder(file))

    assert redis.exists(f"file:{file.id}") == 1
    assert redis.exists(f"owner_id:{file.owner_id}") == 1

def test_read_file_by_id_from_cache(session: Session) -> None:
    file = create_random_file(session=session)

    assert file

    redis.write_file_to_cache(file.id, file.owner_id, jsonable_encoder(file))

    file_obj = redis.read_file_by_id_from_cache(file.id)

    assert file_obj
    assert file_obj["id"] == file.id
    assert file_obj["owner_id"] == file.owner_id
    assert file_obj["name"] == file.name
    assert file_obj["size"] == file.size

def test_read_files_by_owner_id_from_cache(session: Session) -> None:
    user = create_random_user(session=session)

    assert user

    file_1 = create_random_file(session=session, owner_id=user.id)
    file_2 = create_random_file(session=session, owner_id=user.id)

    assert file_1
    assert file_2

    redis.write_file_to_cache(file_1.id, file_1.owner_id, jsonable_encoder(file_1))
    redis.write_file_to_cache(file_2.id, file_2.owner_id, jsonable_encoder(file_2))

    file_objs = redis.read_files_by_owner_id_from_cache(user.id)

    assert len(file_objs) == 2

    for file in file_objs:
        assert file["owner_id"] == user.id

def test_read_file_count_by_owner_id_from_cache(session: Session) -> None:
    user = create_random_user(session=session)

    assert user

    file_1 = create_random_file(session=session, owner_id=user.id)
    file_2 = create_random_file(session=session, owner_id=user.id)

    assert file_1
    assert file_2

    redis.write_file_to_cache(file_1.id, file_1.owner_id, jsonable_encoder(file_1))
    redis.write_file_to_cache(file_2.id, file_2.owner_id, jsonable_encoder(file_2))

    count = redis.read_file_count_by_owner_id_from_cache(user.id)

    assert count == 2

def test_delete_file_from_cache(session: Session) -> None:
    file = create_random_file(session=session)

    assert file

    redis.write_file_to_cache(file.id, file.owner_id, jsonable_encoder(file))

    redis.delete_file_from_cache(file.id)

    assert redis.exists(f"file:{file.id}") == 0
    assert redis.exists(f"owner_id:{file.owner_id}") == 0

    file_obj = redis.read_file_by_id_from_cache(file.id)

    assert not file_obj
