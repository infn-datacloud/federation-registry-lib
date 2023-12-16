"""Network specific fixtures."""
from typing import Any, Dict
from uuid import uuid4

from pytest_cases import fixture, fixture_union, parametrize

from tests.utils.utils import random_bool, random_lower_string, random_positive_int

is_shared = {True, False}
invalid_create_key_values = {
    ("description", None),
    ("uuid", None),
    ("name", None),
    ("is_shared", None),
    ("is_router_external", None),
    ("is_default", None),
    ("mtu", 0),
    ("tags", None),
}


@fixture
def network_create_mandatory_data() -> Dict[str, Any]:
    """Dict with Network mandatory attributes."""
    return {"name": random_lower_string(), "uuid": uuid4()}


@fixture
def network_create_all_data(
    network_create_mandatory_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with all Network attributes."""
    return {
        **network_create_mandatory_data,
        "is_shared": random_bool(),
        "description": random_lower_string(),
        "is_router_external": random_bool(),
        "is_default": random_bool(),
        "mtu": random_positive_int(),
        "proxy_ip": random_lower_string(),
        "proxy_user": random_lower_string(),
        "tags": [random_lower_string()],
    }


@fixture
@parametrize("is_shared", is_shared)
def network_create_data_with_rel(
    network_create_all_data: Dict[str, Any], is_shared: bool
) -> Dict[str, Any]:
    """Dict with relationships attributes.

    Attribute is_shared has been parametrized.
    """
    return {
        **network_create_all_data,
        "is_shared": is_shared,
        "project": None if is_shared else uuid4(),
    }


@fixture
@parametrize("k, v", invalid_create_key_values)
def network_create_invalid_pair(
    network_create_mandatory_data: Dict[str, Any], k: str, v: Any
) -> Dict[str, Any]:
    """Dict with one invalid key-value pair."""
    return {**network_create_mandatory_data, k: v}


@fixture
@parametrize("is_shared", is_shared)
def network_create_invalid_project_conn(
    network_create_mandatory_data: Dict[str, Any], is_shared: bool
) -> Dict[str, Any]:
    """Invalid project list size.

    Invalid cases: If network is marked as public, the list has at least one element,
    if private, the list has no items.
    """
    return {
        **network_create_mandatory_data,
        "is_shared": is_shared,
        "project": None if not is_shared else uuid4(),
    }


network_create_valid_data = fixture_union(
    "network_create_valid_data",
    (network_create_mandatory_data, network_create_data_with_rel),
    idstyle="explicit",
)


network_create_invalid_data = fixture_union(
    "network_create_invalid_data",
    (network_create_invalid_pair, network_create_invalid_project_conn),
    idstyle="explicit",
)
