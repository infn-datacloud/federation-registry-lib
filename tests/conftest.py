from glob import glob
from typing import Any, Dict, Generator, Tuple

import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa
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


def generate_public_private_key_pair() -> Tuple[str, str]:
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    return (public_key, private_key)


(public_key, private_key) = generate_public_private_key_pair()

ALGORITHM = "RS256"
PUBLIC_KEY_ID = "cra1"


def encode_token(payload) -> str:
    return jwt.encode(
        payload=payload,
        key=private_key,
        algorithm=ALGORITHM,
        headers={
            "kid": PUBLIC_KEY_ID,
        },
    )


def get_mock_user_claims(
    sub: str = "", iss: str = "", email: str = ""
) -> Dict[str, Any]:
    return {
        "sub": sub,  # Subject
        "iss": iss,  # Issuer
        "email": email,
        "name": "some-name",
        "groups": ["user-group"],
        "preferred_username": "short-name",
        "organisation_name": "organization-name",
        "exp": 9999999999,  # One long-lasting token, expiring 11/20/2286
        "iat": 0,  # Issued a long time ago: 1/1/1970
        "jti": "JWT Unique ID",
        "client_id": "Client ID",
    }


@pytest.fixture
def client(setup_and_teardown_db: Generator) -> Generator:
    with TestClient(app) as c:
        yield c


MOCK_USER = "test-user"
MOCK_ISSUER = "http://idp.test.it/"
MOCK_READ_EMAIL = "user@test.it"
MOKE_WRITE_EMAIL = "admin@test.it"
FAKE_ISSUER = "http://another-idp.test.it/"


@pytest.fixture()
def api_client_no_sub(client: TestClient) -> TestClient:
    token = encode_token(get_mock_user_claims(iss=MOCK_ISSUER))
    client.headers = {"authorization": f"Bearer {token}"}
    yield client


@pytest.fixture()
def api_client_no_issuer(client: TestClient) -> TestClient:
    token = encode_token(get_mock_user_claims(sub=MOCK_USER))
    client.headers = {"authorization": f"Bearer {token}"}
    yield client


@pytest.fixture()
def api_client_wrong_issuer(client: TestClient) -> TestClient:
    token = encode_token(get_mock_user_claims(sub=MOCK_USER, iss=FAKE_ISSUER))
    client.headers = {"authorization": f"Bearer {token}"}
    yield client


@pytest.fixture()
def api_client_read_only(client: TestClient) -> TestClient:
    token = encode_token(
        get_mock_user_claims(sub=MOCK_USER, iss=MOCK_ISSUER, email=MOCK_READ_EMAIL)
    )
    client.headers = {"authorization": f"Bearer {token}"}
    yield client


@pytest.fixture()
def api_client_read_write(client: TestClient) -> TestClient:
    token = encode_token(
        get_mock_user_claims(sub=MOCK_USER, iss=MOCK_ISSUER, email=MOKE_WRITE_EMAIL)
    )
    client.headers = {
        "authorization": f"Bearer {token}",
        "accept": "application/json",
        "content-type": "application/json",
    }
    yield client
