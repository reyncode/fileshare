from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
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

        return new_user

    def read_user(
        self, *, session: Session, id: int
    ) -> User | None:
        """
        Read the database user by their id.
        """
        return session.scalars(
            select(User).filter_by(id=id)
        ).first()

    def read_user_by_email(
        self, *, session: Session, email: str
    ) -> User | None:
        """
        Read the database user with the email that matches email.
        """
        return session.scalars(
            select(User).filter_by(email=email)
        ).first()

    def update_user(
        self, *, session: Session, db_user: User, user_in: UserUpdate
    ) -> User:
        """
        Update the database user with the details provided in user_in.
        """
        obj_data = jsonable_encoder(db_user)
        update_data = user_in.model_dump(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_user, field, update_data[field])

        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        return db_user

    def update_user_password(
        self, *, session: Session, db_user: User, password: str
    ) -> Message:
        """
        Update the database user's password with a hashed version of password.
        """
        hashed_password = get_password_hash(password)
    
        setattr(db_user, "hashed_password", hashed_password)
    
        session.add(db_user)
        session.commit()
    
        return Message(message="Password updated successfully")

    def delete_user(
        self, *, session: Session, db_user: User
    ) -> Message:
        """
        Delete the database user and all files with their id.
        """
        delete_files = session.scalars(
            select(File).filter_by(owner_id=db_user.id)
        ).all()

        if delete_files:
            for file in delete_files:
                session.delete(file)

        session.delete(db_user)
        session.commit()

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

users = CRUDUsers()
