"""IdentityService specific fixtures."""
from typing import Any, Dict

from pytest_cases import fixture, fixture_union, parametrize

from app.service.enum import ServiceType
from tests.services.identity_service.utils import (
    random_identity_service_all_attr,
    random_identity_service_required_attr,
)

invalid_create_key_values = [
    ("description", None),
    ("type", None),
    ("type", ServiceType.BLOCK_STORAGE),
    ("type", ServiceType.COMPUTE),
    ("type", ServiceType.NETWORK),
    ("endpoint", None),
    ("name", None),
]


@fixture
def identity_service_create_minimum_data() -> Dict[str, Any]:
    """Dict with IdentityService mandatory attributes."""
    return random_identity_service_required_attr()


@fixture
def identity_service_create_all_data() -> Dict[str, Any]:
    """Dict with all IdentityService attributes."""
    return random_identity_service_all_attr()


@fixture
@parametrize("k, v", invalid_create_key_values)
def identity_service_create_invalid_data(k: str, v: Any) -> Dict[str, Any]:
    """Dict with one invalid key-value pair."""
    return {**random_identity_service_required_attr(), k: v}


identity_service_create_valid_data = fixture_union(
    "identity_service_create_valid_data",
    (identity_service_create_minimum_data, identity_service_create_all_data),
    idstyle="explicit",
)
