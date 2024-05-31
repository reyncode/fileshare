from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.crud.file import files
from app.models.file import File
from app.schemas.file import FileCreate, FileUpdate
from app.tests.utils.utils import random_path

def test_create_file(session: Session) -> None:
    path = random_path()

    file_in = FileCreate(path=path)
    file = files.create_file(session=session, file_create=file_in, owner_id=9999)

    assert file
    assert hasattr(file, "path")
    assert file.path == path

def test_read_file(session: Session) -> None:
    path = random_path()

    file_in = FileCreate(path=path)
    file = files.create_file(session=session, file_create=file_in, owner_id=9999)

    read_file = files.read_file(session=session, id=file.id)

    assert read_file
    assert read_file.path == file.path
    assert jsonable_encoder(file) == jsonable_encoder(read_file)

def test_read_file_by_path(session: Session) -> None:
    path = random_path()

    file_in = FileCreate(path=path)
    file = files.create_file(session=session, file_create=file_in, owner_id=9999)

    read_file = files.read_file_by_path(session=session, path=file.path)

    assert read_file
    assert read_file.path == file.path
    assert jsonable_encoder(file) == jsonable_encoder(read_file)

def test_read_all_files_by_user_id(session: Session) -> None:
    file_in_1 = FileCreate(path=random_path())
    file_in_2 = FileCreate(path=random_path())
    file_in_3 = FileCreate(path=random_path())

    file_1 = files.create_file(session=session, file_create=file_in_1, owner_id=8000)
    file_2 = files.create_file(session=session, file_create=file_in_2, owner_id=8000)
    file_3 = files.create_file(session=session, file_create=file_in_3, owner_id=8000)

    file_dict = {
        file_1 : file_1.path,
        file_2 : file_2.path,
        file_3 : file_3.path,
    }

    file_list = files.read_all_files_by_user_id(session=session, user_id=8000)

    assert len(file_dict) == len(file_list)
    for file in file_list:
        assert file in file_dict

def test_read_file_count_by_user_id(session: Session) -> None:
    file_in_1 = FileCreate(path=random_path())
    file_in_2 = FileCreate(path=random_path())

    files.create_file(session=session, file_create=file_in_1, owner_id=9000)
    files.create_file(session=session, file_create=file_in_2, owner_id=9000)

    count = files.read_file_count_by_user_id(session=session, user_id=9000)

    assert count == 2

def test_update_file(session: Session) -> None:
    path = random_path()

    file_in = FileCreate(path=path)
    file = files.create_file(session=session, file_create=file_in, owner_id=9999)

    new_path = random_path()

    updated_file_in = FileUpdate(path=new_path)
    updated_file = files.update_file(session=session, db_file=file, file_in=updated_file_in)

    assert updated_file
    assert updated_file.path == new_path

def test_delete_file(session: Session) -> None:
    path = random_path()

    file_in = FileCreate(path=path)
    file = files.create_file(session=session, file_create=file_in, owner_id=9999)

    files.delete_file(session=session, db_file=file)
    file = files.read_file_by_path(session=session, path=path)

    assert file is None
