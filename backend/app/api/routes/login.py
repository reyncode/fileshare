from datetime import timedelta
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies import SessionDep, CurrentUser
from app.core import security
from app.core.config import settings
from app.crud.user import user_crud
from app.schemas.security import Token
from app.schemas.user import UserPublic

router = APIRouter()

@router.post("/login/access-token")
def login_access_token(
    session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    """
    Validate the user's credentials and create a token if successful.
    """
    user = user_crud.authenticate(
        session=session, email=form_data.username, password=form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password"
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    return Token(
        access_token=security.create_access_token(
            user.id, expires_delta=access_token_expires
        )
    )

@router.post("/login/test-token", response_model=UserPublic)
def test_token(current_user: CurrentUser) -> Any:
    """
    Test access token
    """
    return current_user
