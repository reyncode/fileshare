from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.crud.file import file_crud
from app.tests.utils.file import create_random_file
from app.tests.utils.utils import random_lower_string, random_name

def test_create_file(
    client: TestClient,
    session: Session,
    user_token_headers: dict[str, str],
) -> None:
    name = random_name()
    key = random_lower_string(32)

    data = {
        "name" : name,
        "access_key": key
    }

    r = client.post(
        f"{settings.API_V1_STR}/files/",
        headers=user_token_headers,
        json=data,
    )

    assert r.status_code == 200
    new_file = r.json()
    assert new_file["name"] == name

    r = client.get(
        f"{settings.API_V1_STR}/users/me",
        headers=user_token_headers,
    )

    user_id = r.json()["id"]

    file = file_crud.read_file_by_name(session=session, name=name, owner_id=user_id)

    assert file
    assert file.name == name
    assert file.owner_id == new_file["owner_id"]

def test_create_file_duplicate_names(
    client: TestClient,
    session: Session,
    user_token_headers: dict[str, str],
) -> None:
    name = "file.png"
    size = 648
    key_1 = random_lower_string(32)
    key_2 = random_lower_string(32)
    key_3 = random_lower_string(32)

    file_data_1 = {
        "name": name,
        "access_key": key_1,
        "size": size
    }

    file_data_2 = {
        "name": name,
        "access_key": key_2,
        "size": size
    }

    file_data_3 = {
        "name": name,
        "access_key": key_3,
        "size": size
    }

    files_data = [file_data_1, file_data_2, file_data_3]
    for file_data in files_data:
        r = client.post(
            f"{settings.API_V1_STR}/files/",
            headers=user_token_headers,
            json=file_data,
        )
        assert r.status_code == 200

    r = client.get(
        f"{settings.API_V1_STR}/users/me",
        headers=user_token_headers,
    )

    user_id = r.json()["id"]

    file_1 = file_crud.read_file_by_name(session=session, name="file.png", owner_id=user_id)
    file_2 = file_crud.read_file_by_name(session=session, name="file_1.png", owner_id=user_id)
    file_3 = file_crud.read_file_by_name(session=session, name="file_2.png", owner_id=user_id)

    assert file_1
    assert file_2
    assert file_3

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
    assert new_file["name"] == file.name
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

    data = {"name": "some-file.txt"}

    r = client.put(
        f"{settings.API_V1_STR}/files/{file.id}",
        headers=user_token_headers,
        json=data,
    ) 

    assert r.status_code == 200, f"{r.json()['detail']}"
    updated_file = r.json()
    assert updated_file["name"] == "some-file.txt"
    assert updated_file["owner_id"] == file.owner_id

def test_update_file_not_found_error(
    client: TestClient, user_token_headers: dict[str, str]
) -> None:
    data = {"name": "missing.txt"}

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
    data = {"name": file.name}

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
