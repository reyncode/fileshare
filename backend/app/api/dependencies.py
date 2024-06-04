from collections.abc import Generator
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core import security
from app.core.config import settings
from app.crud.user import user_crud
from app.database.core import engine
from app.models.user import User
from app.schemas.security import TokenPayload

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)

def get_database_session() -> Generator[Session, None, None]:
    """
    Start a session with the database.
    """
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_database_session)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]

def get_current_user(
    session: SessionDep, token: TokenDep
) -> User:
    """
    Get's the current user after validating the user's credientails.
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except(JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials"
        )

    user = user_crud.read_user(session=session, id=token_data.sub) # type: ignore

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user

CurrentUser = Annotated[User, Depends(get_current_user)]
