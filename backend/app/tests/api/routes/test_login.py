from unittest.mock import patch

from fastapi.testclient import TestClient

from app.core.config import settings

def test_get_access_token(client: TestClient) -> None:
    login_data = {
        "username": settings.TEST_USER_EMAIL,
        "password": settings.TEST_USER_PASSWORD,
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()

    assert r.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]

def test_get_access_token_incorrect_password(client: TestClient) -> None:
    login_data = {
        "username": settings.TEST_USER_EMAIL,
        "password": "incorrect",
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)

    assert r.status_code == 400

def test_use_access_token(
    client: TestClient, user_token_headers: dict[str, str]
) -> None:
    r = client.post(
        f"{settings.API_V1_STR}/login/test-token",
        headers=user_token_headers,
    )
    result = r.json()

    assert r.status_code == 200
    assert "email" in result
