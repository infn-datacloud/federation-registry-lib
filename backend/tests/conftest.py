import subprocess
from glob import glob
from typing import Dict, Generator

import pytest
from fastapi.testclient import TestClient
from neomodel import clear_neo4j_database, db

from app.main import app


def refactor(string: str) -> str:
    return string.replace("/", ".").replace("\\", ".").replace(".py", "")


pytest_plugins = [refactor(fixture) for fixture in glob("tests/fixtures/[!__]*.py")]

pytest.register_assert_rewrite("tests.utils")


# DB specific fixtures


@pytest.fixture
def setup_and_teardown_db() -> Generator:
    clear_neo4j_database(db)
    yield
    clear_neo4j_database(db)


# API specific fixtures


@pytest.fixture
def client(setup_and_teardown_db: Generator) -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture
def token() -> str:
    issuer = "https://iam.cloud.infn.it/"
    token_cmd = subprocess.run(
        [
            "docker",
            "exec",
            "catalog-api-oidc-agent-1",
            "oidc-token",
            issuer,
        ],
        stdout=subprocess.PIPE,
        text=True,
    )
    yield token_cmd.stdout.strip("\n")


@pytest.fixture
def read_header(token: str) -> Dict:
    return {"authorization": f"Bearer {token}"}


@pytest.fixture
def write_header(read_header: Dict) -> Dict:
    return {
        **read_header,
        "accept": "application/json",
        "content-type": "application/json",
    }
