from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.crud.user import user_crud
from app.core.config import settings
from app.models.user import User
from app.schemas.user import UserCreate
from app.tests.utils.utils import random_email, random_lower_string

def get_user_token_headers(client: TestClient) -> dict[str, str]:
    login_data = {
        "username": settings.TEST_USER_EMAIL,
        "password": settings.TEST_USER_PASSWORD,
    }

    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}

    return headers

def create_random_user(session: Session) -> User:
    email = random_email()
    password = random_lower_string(32)
    user_in = UserCreate(email=email, password=password)
    user = user_crud.create_user(session=session, user_create=user_in)

    return user
