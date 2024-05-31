from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.tests.core.database import SessionTesting, engine, init_db
from app.api.dependencies import get_database_session
from app.tests.utils.user import get_user_token_headers

@pytest.fixture(scope="session", autouse=True)
def session() -> Generator[Session, None, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)

    init_db(session=session)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="module")
def client(session) -> Generator[TestClient, None, None]:
    def override_get_database_session():
        yield session
    
    app.dependency_overrides[get_database_session] = override_get_database_session

    yield TestClient(app)

    del app.dependency_overrides[get_database_session]

@pytest.fixture(scope="module")
def user_token_headers(client: TestClient) -> dict[str, str]:
    return get_user_token_headers(client)
