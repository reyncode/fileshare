from unittest.mock import patch

from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.crud.user import user_crud
from app.models.user import User
from app.core.security import verify_password
from app.schemas.user import UserCreate, UserUpdate
from app.tests.utils.utils import random_email, random_lower_string

def test_register_user(client: TestClient, session: Session) -> None:
    with patch("app.core.config.settings.USERS_OPEN_REGISTRATION", True):
        username = random_email()
        password = random_lower_string(32)

        data = {"email": username, "password": password}
        r = client.post(
            f"{settings.API_V1_STR}/users/register",
            json=data,
        )

        assert r.status_code == 200
        created_user = r.json()
        assert created_user["email"] == username

        user = user_crud.read_user_by_email(session=session, email=username)

        assert user
        assert user.email == username
        assert verify_password(password, user.hashed_password)

def test_register_user_closed_registration_error(
    client: TestClient
) -> None:
    with patch("app.core.config.settings.USERS_OPEN_REGISTRATION", False):
        username = random_email()
        password = random_lower_string(32)

        data = {"email": username, "password": password}
        r = client.post(
            f"{settings.API_V1_STR}/users/register",
            json=data,
        )

        assert r.status_code == 403
        assert r.json()["detail"] == "Open user registration is forbidden on this server"

def test_register_user_already_exists_error(
    client: TestClient
) -> None:
    data = {"email": settings.TEST_USER_EMAIL, "password": settings.TEST_USER_PASSWORD}
    r = client.post(
        f"{settings.API_V1_STR}/users/register",
        json=data,
    )

    assert r.status_code == 400
    assert r.json()["detail"] == "A user with this email aready exists"

def test_read_user_me(
    client: TestClient,
    user_token_headers: dict[str, str]
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=user_token_headers)
    current_user = r.json()

    assert current_user
    assert current_user["email"] == settings.TEST_USER_EMAIL

def test_update_user_me(
    client: TestClient, user_token_headers: dict[str, str], session: Session
) -> None:
    email = random_email()

    data = {"email": email}

    r = client.patch(
        f"{settings.API_V1_STR}/users/me",
        headers=user_token_headers,
        json=data,
    )

    assert r.status_code == 200
    updated_user = r.json()
    assert updated_user["email"] == email

    # revert the email until we figure out the rollback

    user = user_crud.read_user_by_email(session=session, email=email)

    user_in = UserUpdate(email=settings.TEST_USER_EMAIL)
    if user:
        user = user_crud.update_user(session=session, user_id=user.id, user_in=user_in)

    session.refresh(user)

    assert r.status_code == 200
    assert user
    assert user.email == settings.TEST_USER_EMAIL

def test_update_user_me_email_already_exists_error(
    client: TestClient, user_token_headers: dict[str, str]
) -> None:
    data = {"email": settings.TEST_USER_EMAIL}
    r = client.patch(
        f"{settings.API_V1_STR}/users/me",
        headers=user_token_headers,
        json=data,
    )

    assert r.status_code == 409
    assert r.json()["detail"] == "User with this email already exists"

def test_update_password_me(
    client: TestClient, user_token_headers: dict[str, str], session: Session
) -> None:
    new_password = random_lower_string(32)
    data = {
        "current_password": settings.TEST_USER_PASSWORD,
        "new_password": new_password,
    }

    r = client.patch(
        f"{settings.API_V1_STR}/users/me/password",
        headers=user_token_headers,
        json=data,
    )

    assert r.status_code == 200
    updated_user = r.json()
    assert updated_user["message"] == "Password updated successfully"

    user = session.scalars(
        select(User).filter_by(email=settings.TEST_USER_EMAIL)
    ).first()

    assert user
    assert user.email == settings.TEST_USER_EMAIL
    assert verify_password(new_password, user.hashed_password)

    # revert the password until we figure out the rollback

    data = {
        "current_password": new_password,
        "new_password": settings.TEST_USER_PASSWORD,
    }

    r = client.patch(
        f"{settings.API_V1_STR}/users/me/password",
        headers=user_token_headers,
        json=data,
    )

    assert r.status_code == 200, f"{r.json()['detail']}"
    assert verify_password(settings.TEST_USER_PASSWORD, user.hashed_password)

def test_update_password_me_incorrect_password_error(
    client: TestClient, user_token_headers: dict[str, str]
) -> None:
    data = {
        "current_password": "wrong",
        "new_password": "secret",
    }

    r = client.patch(
        f"{settings.API_V1_STR}/users/me/password",
        headers=user_token_headers,
        json=data,
    )

    assert r.status_code == 400
    assert r.json()["detail"] == "Incorrect password"

def test_update_password_me_same_password_error(
    client: TestClient, user_token_headers: dict[str, str]
) -> None:
    data = {
        "current_password": settings.TEST_USER_PASSWORD,
        "new_password": settings.TEST_USER_PASSWORD,
    }

    r = client.patch(
        f"{settings.API_V1_STR}/users/me/password",
        headers=user_token_headers,
        json=data,
    )

    assert r.status_code == 400
    assert r.json()["detail"] == "New password cannot be the same as the current password"

def test_delete_user_me(
    client: TestClient, user_token_headers: dict[str, str], session: Session
) -> None:
    
    r = client.delete(
        f"{settings.API_V1_STR}/users/me",
        headers=user_token_headers,
    )

    user = session.scalars(
        select(User).filter_by(email=settings.TEST_USER_EMAIL)
    ).first()

    assert r.status_code == 200
    assert user is None

    # revert the user delete until we figure out the rollback

    user_in = UserCreate(email=settings.TEST_USER_EMAIL, password=settings.TEST_USER_PASSWORD)
    user = user_crud.create_user(session=session, user_create=user_in)

    assert r.status_code == 200
    assert user
    assert user.email == settings.TEST_USER_EMAIL
    assert verify_password(settings.TEST_USER_PASSWORD, user.hashed_password)
