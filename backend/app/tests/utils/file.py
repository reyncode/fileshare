from sqlalchemy.orm import Session

from app.crud.file import files
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_path
from app.models.file import File
from app.schemas.file import FileCreate

def create_random_file(session: Session, owner_id: int | None = None) -> File:
    path = random_path()
    file_in = FileCreate(path=path)

    if owner_id:
        file = files.create_file(session=session, file_create=file_in, owner_id=owner_id)
    else:
        user = create_random_user(session)
        file = files.create_file(session=session, file_create=file_in, owner_id=user.id)

    return file
