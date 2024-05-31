from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.file import File
from app.schemas.file import FileCreate, FileUpdate
from app.schemas.security import Message

class CRUDFiles():
    def create_file(
        self, *, session: Session, file_create: FileCreate, owner_id: int
    ) -> File:
        """
        Create a new database file.
        """
        # TODO: logic to determine if this is a folder or file

        new_file = File(
            path=file_create.path,
            owner_id=owner_id,
            created_at=func.now(),
            updated_at=func.now(),
        )

        session.add(new_file)
        session.commit()
        session.refresh(new_file)

        return new_file

    def read_file(
        self, *, session: Session, id: int
    ) -> File | None:
        """
        Read the database file by it's id.
        """
        return session.scalars(
            select(File).filter_by(id=id)
        ).first()

    def read_file_by_path(
        self, *, session: Session, path: str
    ) -> File | None:
        """
        Read the database file by it's path.
        """
        return session.scalars(
            select(File).filter_by(path=path)
        ).first()

    def read_all_files_by_user_id(
        self, *, session: Session, user_id: int, skip: int = 0, limit: int = 25
        ) -> List[File]:
        """
        Read all the database file's that have an owner_id of user_id.
        """
        return session.scalars(
            select(File).filter_by(owner_id=user_id).offset(skip).limit(limit)
        ).all() # type: ignore

    def read_file_count_by_user_id(
        self, *, session: Session, user_id: int
    ) -> int:
        count = session.scalar(
            select(func.count()).select_from(File).where(File.owner_id == user_id)
        )

        return 0 if count == None else count

    def update_file(
        self, *, session: Session, db_file: File, file_in: FileUpdate
    ) -> File:
        """
        Update the database file with the details provided in file_in.
        """
        obj_data = jsonable_encoder(db_file)
        update_data = file_in.model_dump(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_file, field, update_data[field])

        session.add(db_file)
        session.commit()
        session.refresh(db_file)
    
        return db_file

    def delete_file(
        self, *, session: Session, db_file: File
    ) -> Message:
        """
        Delete the database file.
        """
        session.delete(db_file)
        session.commit()

        return Message(message="File deleted successfully")

files = CRUDFiles()
