from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.crud.file import file_crud
from app.schemas.file import FileCreate, FileUpdate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_name, random_lower_string
from app.tests.utils.file import create_random_file

def test_create_file(session: Session) -> None:
    user = create_random_user(session=session)

    assert user

    name = random_name()
    key = random_lower_string(32)

    file_in = FileCreate(name=name, access_key=key)
    file = file_crud.create_file(session=session, file_in=file_in, owner_id=user.id)

    assert file
    assert hasattr(file, "name")
    assert hasattr(file, "size")
    assert file.name == name
    assert file.size == 0

def test_create_files_same_name_different_user(session: Session) -> None:
    name = "file.png"
    size = 648
    key_1 = random_lower_string(32)
    key_2 = random_lower_string(32)

    file_in_1 = FileCreate(name=name, access_key=key_1, size=size)
    file_in_2 = FileCreate(name=name, access_key=key_2, size=size)

    user_1 = create_random_user(session=session)
    user_2 = create_random_user(session=session)

    assert user_1
    assert user_2

    file_1 = file_crud.create_file(session=session, file_in=file_in_1, owner_id=user_1.id)
    file_2 = file_crud.create_file(session=session, file_in=file_in_2, owner_id=user_2.id)

    assert file_1
    assert file_2
    assert file_1.name == name
    assert file_2.name == name
    assert file_1.size == size
    assert file_2.size == size
    assert file_1.owner_id != file_2.owner_id

def test_read_file(session: Session) -> None:
    file = create_random_file(session=session)

    assert file

    read_file = file_crud.read_file(session=session, id=file.id)

    assert read_file
    assert read_file.name == file.name
    assert jsonable_encoder(file) == jsonable_encoder(read_file)

def test_read_file_by_name(session: Session) -> None:
    file = create_random_file(session=session)

    assert file

    read_file = file_crud.read_file_by_name(session=session, name=file.name, owner_id=file.owner_id)

    assert read_file
    assert read_file.name == file.name
    assert read_file.size == file.size
    assert jsonable_encoder(file) == jsonable_encoder(read_file)

def test_read_all_files_by_owner_id(session: Session) -> None:
    user = create_random_user(session=session)

    assert user

    file_1 = create_random_file(session=session, owner_id=user.id)
    file_2 = create_random_file(session=session, owner_id=user.id)

    assert file_1
    assert file_2

    file_dict = {
        file_1.id : file_1.name,
        file_2.id : file_2.name,
    }

    file_list = file_crud.read_all_files_by_owner_id(session=session, user_id=user.id)

    assert len(file_dict) == len(file_list)
    assert jsonable_encoder(file_list[0]) != jsonable_encoder(file_list[1])
    for file in file_list:
        assert file.id in file_dict

def test_read_file_count_by_owner_id(session: Session) -> None:
    user = create_random_user(session=session)

    assert user

    file_1 = create_random_file(session=session, owner_id=user.id)
    file_2 = create_random_file(session=session, owner_id=user.id)

    assert file_1
    assert file_2

    count = file_crud.read_file_count_by_owner_id(session=session, user_id=user.id)

    assert count == 2

def test_update_file(session: Session) -> None:
    file = create_random_file(session=session)

    assert file

    new_name = random_name()
    new_size = 886

    updated_file_in = FileUpdate(name=new_name, size=new_size)
    updated_file = file_crud.update_file(session=session, file_id=file.id, file_in=updated_file_in)

    assert updated_file
    assert updated_file.name == new_name
    assert updated_file.size == new_size

def test_delete_file(session: Session) -> None:
    user = create_random_user(session=session)

    assert user

    file = create_random_file(session=session, owner_id=user.id)

    assert file

    file_crud.delete_file(session=session, file_id=file.id)
    result = file_crud.read_file_by_name(session=session, name=file.name, owner_id=user.id)

    assert result is None
