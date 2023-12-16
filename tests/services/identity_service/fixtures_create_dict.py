"""IdentityService specific fixtures."""
from typing import Any, Dict

from pytest_cases import fixture, parametrize

from app.service.enum import ServiceType
from tests.common.utils import random_lower_string, random_url
from tests.services.utils import random_identity_service_name

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
def identity_service_create_mandatory_data() -> Dict[str, Any]:
    """Dict with IdentityService mandatory attributes."""
    return {"endpoint": random_url(), "name": random_identity_service_name()}


@fixture
def identity_service_create_valid_data(
    identity_service_create_mandatory_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with all IdentityService attributes.

    Attribute is_public has been parametrized.
    """
    return {
        **identity_service_create_mandatory_data,
        "description": random_lower_string(),
    }


@fixture
@parametrize("k, v", invalid_create_key_values)
def identity_service_create_invalid_data(
    identity_service_create_mandatory_data: Dict[str, Any], k: str, v: Any
) -> Dict[str, Any]:
    """Dict with one invalid key-value pair."""
    data = {**identity_service_create_mandatory_data}
    data[k] = v
    return data
