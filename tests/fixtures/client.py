from typing import Any, Dict, Generator, Optional, Tuple, Type

import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa
from fastapi.testclient import TestClient
from pydantic import AnyHttpUrl, BaseModel, EmailStr

from app.main import app

# API specific fixtures


ALGORITHM = "RS256"
PUBLIC_KEY_ID = "cra1"

MOCK_USER = "test-user"
MOCK_ISSUER = "http://idp.test.it/"
MOCK_READ_EMAIL = "user@test.it"
MOKE_WRITE_EMAIL = "admin@test.it"
FAKE_ISSUER = "http://another-idp.test.it/"


class User(BaseModel):
    sub: Optional[str]
    iss: Optional[AnyHttpUrl]
    email: Optional[EmailStr]


def generate_public_private_key_pair() -> Tuple[str, str]:
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    return (public_key, private_key)


(public_key, private_key) = generate_public_private_key_pair()


def encode_token(payload) -> str:
    return jwt.encode(
        payload=payload,
        key=private_key,
        algorithm=ALGORITHM,
        headers={"kid": PUBLIC_KEY_ID},
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
    """
    API Client with no token.
    """
    with TestClient(app) as c:
        yield c


@pytest.fixture(
    params=[
        None,
        User(iss=MOCK_ISSUER, email=MOCK_READ_EMAIL),
        User(sub=MOCK_USER, email=MOCK_READ_EMAIL),
        User(sub=MOCK_USER, iss=FAKE_ISSUER, email=MOCK_READ_EMAIL),
        User(sub=MOCK_USER, iss=MOCK_ISSUER, email=MOCK_READ_EMAIL),
    ]
)
def api_client_read_only(
    client: TestClient, request: Type[pytest.FixtureRequest]
) -> TestClient:
    """
    API client with only read access rights.

    1. No token
    2. Invalid token: lost sub.
    3. Invalid token: lost iss.
    4. Invalid token: the iss does not exist.
    5. Valid token but the subject has an email with only read
    access rights.
    """
    if request.param:
        token = encode_token(
            get_mock_user_claims(
                sub=request.param.sub, iss=request.param.iss, email=request.param.email
            )
        )
        client.headers = {"authorization": f"Bearer {token}"}
    yield client


@pytest.fixture()
def api_client_read_write(client: TestClient) -> TestClient:
    """
    API client with read and write access rights.
    """
    token = encode_token(
        get_mock_user_claims(sub=MOCK_USER, iss=MOCK_ISSUER, email=MOKE_WRITE_EMAIL)
    )
    client.headers = {
        "authorization": f"Bearer {token}",
        "accept": "application/json",
        "content-type": "application/json",
    }
    yield client
