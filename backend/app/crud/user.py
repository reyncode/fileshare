from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.cache.core import redis_db as redis
from app.core.security import get_password_hash, verify_password
from app.crud.file import file_crud
from app.models.file import File
from app.models.user import User
from app.schemas.security import Message
from app.schemas.user import UserCreate, UserUpdate

class CRUDUsers():
    def create_user(
        self, *, session: Session, user_create: UserCreate
    ) -> User:
        """
        Create a new database user.
        """
        hashed_password = get_password_hash(user_create.password)

        new_user = User(
            email=user_create.email,
            hashed_password=hashed_password,
            created_at=func.now(),
            updated_at=func.now(),
        )

        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        redis.write_user_to_cache(new_user.id, new_user.email, jsonable_encoder(new_user))

        return new_user

    def read_user(
        self, *, session: Session, id: int
    ) -> User | None:
        """
        Read the database user by their id.
        """
        user_obj = redis.read_user_by_id_from_cache(id)
        if user_obj:
            return User(**user_obj)

        user = session.scalars(
            select(User).filter_by(id=id)
        ).first()

        if user:
            redis.write_user_to_cache(user.id, user.email, jsonable_encoder(user))

        return user

    def read_user_by_email(
        self, *, session: Session, email: str
    ) -> User | None:
        """
        Read the database user with the email that matches email.
        """
        user_obj = redis.read_user_by_email_from_cache(email)
        if user_obj:
            return User(**user_obj)

        user = session.scalars(
            select(User).filter_by(email=email)
        ).first()

        if user:
            redis.write_user_to_cache(user.id, user.email, jsonable_encoder(user))

        return user

    def update_user(
        self, *, session: Session, user_id: int, user_in: UserUpdate
    ) -> User:
        """
        Update the database user with the details provided in user_in.
        """
        user = session.get(User, user_id)

        obj_data = jsonable_encoder(user)
        update_data = user_in.model_dump(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(user, field, update_data[field])

        session.add(user)
        session.commit()
        session.refresh(user)

        if "email" in obj_data:
            redis.delete_user_from_cache(user_id)

        redis.write_user_to_cache(user_id, user.email, jsonable_encoder(user)) # type: ignore

        return user

    def update_user_password(
        self, *, session: Session, user_id: int, password: str
    ) -> Message:
        """
        Update the database user's password with a hashed version of password.
        """
        user = session.get(User, user_id)

        hashed_password = get_password_hash(password)
    
        setattr(user, "hashed_password", hashed_password)
    
        session.add(user)
        session.commit()
        session.refresh(user)

        redis.write_user_to_cache(user.id, user.email, jsonable_encoder(user)) # type: ignore
    
        return Message(message="Password updated successfully")

    def delete_user(
        self, *, session: Session, user_id: int
    ) -> Message:
        """
        Delete the database user and all files with their id.
        """
        user = session.get(User, user_id)

        file_ids = session.scalars(
            select(File.id).filter_by(owner_id=user.id) # type: ignore
        ).all()

        for id in file_ids:
            file_crud.delete_file(session=session, file_id=id)

        session.delete(user)
        session.commit()

        redis.delete_user_from_cache(user.id) # type: ignore

        return Message(message="User deleted successfully")

    def authenticate(
        self, *, session: Session, email: str, password: str
    ) -> User | None:
        """
        Authenticate the database user with the email and password credentials.
        """
        user = self.read_user_by_email(session=session, email=email)
        if not user:
            return None

        is_authenticated = verify_password(password, user.hashed_password)
        if not is_authenticated:
            return None

        return user

user_crud = CRUDUsers()
