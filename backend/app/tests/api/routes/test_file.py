from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.crud.file import file_crud
from app.tests.utils.file import create_random_file
from app.tests.utils.utils import random_path

def test_create_file(
    client: TestClient,
    session: Session,
    user_token_headers: dict[str, str],
) -> None:
    path = random_path()

    data = {"path" : path}

    r = client.post(
        f"{settings.API_V1_STR}/files/",
        headers=user_token_headers,
        json=data,
    )

    assert r.status_code == 200
    new_file = r.json()
    assert new_file["path"] == path

    r = client.get(
        f"{settings.API_V1_STR}/users/me",
        headers=user_token_headers,
    )

    user_id = r.json()["id"]

    file = file_crud.read_file_by_path(session=session, path=path, owner_id=user_id)

    assert file
    assert file.path == path
    assert file.owner_id == new_file["owner_id"]

def test_create_file_already_exists_error(
    client: TestClient, session: Session, user_token_headers: dict[str, str]
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/users/me",
        headers=user_token_headers,
    )

    assert r.status_code == 200

    user_id = r.json()["id"]

    file = create_random_file(session=session, owner_id=user_id)

    data = {"path": file.path}

    r = client.post(
        f"{settings.API_V1_STR}/files/",
        headers=user_token_headers,
        json=data,
    )

    assert r.status_code == 400
    assert r.json()["detail"] == "A file with the same name already exists"

def test_read_file(
    client: TestClient, session: Session, user_token_headers: dict[str, str]
) -> None:
    file = create_random_file(session=session)

    r = client.get(
        f"{settings.API_V1_STR}/files/{file.id}",
        headers=user_token_headers,
    ) 

    assert r.status_code == 200
    new_file = r.json()
    assert new_file["path"] == file.path
    assert new_file["owner_id"] == file.owner_id

def test_read_file_not_found_error(
    client: TestClient, user_token_headers: dict[str, str]
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/files/566",
        headers=user_token_headers,
    ) 

    assert r.status_code == 404
    assert r.json()["detail"] == "File not found"

def test_read_files(
    client: TestClient, session: Session, user_token_headers: dict[str, str]
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/users/me",
        headers=user_token_headers,
    )

    assert r.status_code == 200

    user_id = r.json()["id"]

    create_random_file(session=session, owner_id=user_id)
    create_random_file(session=session, owner_id=user_id)
    create_random_file(session=session, owner_id=user_id)

    r = client.get(
        f"{settings.API_V1_STR}/files/",
        headers=user_token_headers,
    )

    assert r.status_code == 200
    content = r.json()
    assert len(content["data"]) >= 3

def test_update_file(
    client: TestClient, session: Session, user_token_headers: dict[str, str]
) -> None:
    """
    Get the id of the current user, create a file using the users id as the owner_id 
    and then update the file.
    """
    r = client.get(
        f"{settings.API_V1_STR}/users/me",
        headers=user_token_headers,
    )

    assert r.status_code == 200

    user_id = r.json()["id"]

    file = create_random_file(session=session, owner_id=user_id)

    data = {"path": "/some/updated/path.txt"}

    r = client.put(
        f"{settings.API_V1_STR}/files/{file.id}",
        headers=user_token_headers,
        json=data,
    ) 

    assert r.status_code == 200, f"{r.json()['detail']}"
    updated_file = r.json()
    assert updated_file["path"] == "/some/updated/path.txt"
    assert updated_file["owner_id"] == file.owner_id

def test_update_file_not_found_error(
    client: TestClient, user_token_headers: dict[str, str]
) -> None:
    data = {"path": "/some/unknown/path.txt"}

    r = client.put(
        f"{settings.API_V1_STR}/files/666",
        headers=user_token_headers,
        json=data,
    ) 

    assert r.status_code == 404
    assert r.json()["detail"] == "File not found"

def test_update_file_not_enough_permissions_error(
    client: TestClient, session: Session, user_token_headers: dict[str, str]
) -> None:
    """
    The current user is not the owner of this file.
    """
    file = create_random_file(session=session)
    data = {"path": file.path}

    r = client.put(
        f"{settings.API_V1_STR}/files/{file.id}",
        headers=user_token_headers,
        json=data,
    ) 

    assert r.status_code == 400
    assert r.json()["detail"] == "User does not have permission to update this file"

def test_delete_file(
    client: TestClient, session: Session, user_token_headers: dict[str, str]
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/users/me",
        headers=user_token_headers,
    )

    assert r.status_code == 200

    user_id = r.json()["id"]

    file = create_random_file(session=session, owner_id=user_id)

    r = client.delete(
        f"{settings.API_V1_STR}/files/{file.id}",
        headers=user_token_headers,
    )

    assert r.status_code == 200, f"{r.json()['detail']}"
    assert r.json()["message"] == "File deleted successfully"

def test_delete_file_not_found_error(
    client: TestClient, user_token_headers: dict[str, str]
) -> None:
    r = client.delete(
        f"{settings.API_V1_STR}/files/999",
        headers=user_token_headers,
    ) 

    assert r.status_code == 404
    assert r.json()["detail"] == "File not found"

def test_delete_file_not_enough_permissions_error(
    client: TestClient, session: Session, user_token_headers: dict[str, str]
) -> None:
    """
    The current user is not the owner of this file.
    """
    file = create_random_file(session=session)

    r = client.delete(
        f"{settings.API_V1_STR}/files/{file.id}",
        headers=user_token_headers,
    )

    assert r.status_code == 400
    assert r.json()["detail"] == "User does not have permission to delete this file"
