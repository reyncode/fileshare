from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.cache.core import redis_db as redis
from app.models.file import File
from app.schemas.file import FileCreate, FileUpdate
from app.schemas.security import Message

class CRUDFiles():
    def create_file(
        self, *, session: Session, file_in: FileCreate, owner_id: int
    ) -> File:
        """
        Create a new database file.
        """
        new_file = File(
            name=file_in.name,
            access_key=file_in.access_key,
            size=file_in.size,
            owner_id=owner_id,
            created_at=func.now(),
            updated_at=func.now(),
        )

        session.add(new_file)
        session.commit()
        session.refresh(new_file)

        redis.write_file_to_cache(new_file.id, new_file.owner_id, jsonable_encoder(new_file))

        return new_file

    def read_file(
        self, *, session: Session, id: int
    ) -> File | None:
        """
        Read the database file by it's id.
        """
        file_obj = redis.read_file_by_id_from_cache(id)
        if file_obj:
            return File(**file_obj)

        file = session.scalars(
            select(File).filter_by(id=id)
        ).first()

        if file:
            redis.write_file_to_cache(file.id, file.owner_id, jsonable_encoder(file))

        return file

    def read_file_by_name(
        self, *, session: Session, name: str, owner_id: int
    ) -> File | None:
        """
        Read the database file by it's name for the provided owner_id.
        """
        return session.scalars(
            select(File).filter_by(name=name, owner_id=owner_id)
        ).first()

    def read_file_count_by_owner_id(
        self, *, session: Session, user_id: int
    ) -> int:
        count = session.scalar(
            select(func.count()).select_from(File).where(File.owner_id == user_id)
        )

        return 0 if count == None else count

    def read_all_files_by_owner_id(
        self, *, session: Session, user_id: int, skip: int = 0, limit: int = 25
        ) -> List[File]:
        """
        Read all the database file's that have an owner_id of user_id.
        """
        database_file_count = self.read_file_count_by_owner_id(session=session, user_id=user_id)
        cached_file_count = redis.read_file_count_by_owner_id_from_cache(user_id)

        if database_file_count == cached_file_count:
            file_objs = redis.read_files_by_owner_id_from_cache(user_id)
            if file_objs:
                return [File(**file) for file in file_objs]

        files = session.scalars(
            select(File).filter_by(owner_id=user_id).offset(skip).limit(limit)
        ).all()

        for file in files:
            redis.write_file_to_cache(file.id, file.owner_id, jsonable_encoder(file))

        return files # type: ignore

    def update_file(
        self, *, session: Session, file_id: int, file_in: FileUpdate
    ) -> File:
        """
        Update the database file with the details provided in file_in.
        """
        file = session.get(File, file_id)

        obj_data = jsonable_encoder(file)
        update_data = file_in.model_dump(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(file, field, update_data[field])

        session.add(file)
        session.commit()
        session.refresh(file)

        redis.write_file_to_cache(file.id, file.owner_id, jsonable_encoder(file)) # type: ignore
    
        return file

    def delete_file(
        self, *, session: Session, file_id: int
    ) -> Message:
        """
        Delete the database file.
        """
        file = session.get(File, file_id)

        session.delete(file)
        session.commit()

        redis.delete_file_from_cache(file_id)

        return Message(message="File deleted successfully")

    def generate_unique_name(
        self, *, session: Session, name: str, owner_id: int
    ) -> str:
        base, extension = name.rsplit('.', 1)

        existing_names = session.scalars(
            select(File.name).filter(File.name.like(f"{base}%")).where(File.owner_id == owner_id)
        ).all()

        if name not in existing_names:
            return name

        i = 1
        while True:
            new_name = f"{base}_{i}.{extension}"
            if new_name not in existing_names:
                return new_name
            i += 1

file_crud = CRUDFiles()
