from typing import Any

from fastapi import APIRouter, HTTPException

from app.api.dependencies import CurrentUser, SessionDep
from app.core.config import settings
from app.core.security import verify_password
from app.crud.user import user_crud
from app.schemas.security import Message
from app.schemas.user import (
    UpdatePassword,
    UserCreate,
    UserPublic,
    UserUpdate,
)
from app.schemas.utils import to_pydantic

router = APIRouter()

@router.post("/register", response_model=UserPublic)
def register_user(session: SessionDep, user_in: UserCreate) -> Any:
    """
    Create a new user with the provided credentials.
    """
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=403,
            detail="Open user registration is forbidden on this server"
        )

    user = user_crud.read_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="A user with this email aready exists"
        )

    user_create = UserCreate.model_validate(user_in.model_dump(exclude_unset=True))
    user = user_crud.create_user(session=session, user_create=user_create)

    return user

@router.get("/me", response_model=UserPublic)
def read_user_me(current_user: CurrentUser) -> Any:
    """
    Get the current user.
    """
    return to_pydantic(current_user, UserPublic)

@router.patch("/me", response_model=UserPublic)
def update_user_me(
    *, session: SessionDep, user_in: UserUpdate, current_user: CurrentUser
) -> Any:
    """
    Update the current user.
    """
    if user_in.email:
        if user_crud.read_user_by_email(session=session, email=user_in.email):
            raise HTTPException(
                status_code=409,
                detail="User with this email already exists"
            )

    user = user_crud.update_user(session=session, user_id=current_user.id, user_in=user_in)

    return to_pydantic(user, UserPublic)

@router.patch("/me/password", response_model=Message)
def update_password_me(
    *, session: SessionDep, body: UpdatePassword, current_user: CurrentUser
) -> Any:
    """
    Update the current users password
    """
    if not verify_password(body.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=400,
            detail="Incorrect password"
        )

    if body.current_password == body.new_password:
        raise HTTPException(
            status_code=400,
            detail="New password cannot be the same as the current password"
        )

    return user_crud.update_user_password(session=session, user_id=current_user.id, password=body.new_password)

@router.delete("/me", response_model=Message)
def delete_user_me(
    *, session: SessionDep, current_user: CurrentUser
) -> Any:
    """
    Delete own user.
    """
    return user_crud.delete_user(session=session, user_id=current_user.id)
