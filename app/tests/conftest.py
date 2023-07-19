import pytest
from fastapi.testclient import TestClient
from neomodel import clear_neo4j_database, db
from typing import Generator

from app.main import app


@pytest.fixture
def setup_and_teardown_db() -> Generator:
    clear_neo4j_database(db)
    yield
    clear_neo4j_database(db)


@pytest.fixture
def client(setup_and_teardown_db: Generator) -> Generator:
    with TestClient(app) as c:
        yield c
