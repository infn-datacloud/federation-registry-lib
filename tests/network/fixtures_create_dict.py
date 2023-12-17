"""Network specific fixtures."""
from typing import Any, Dict
from uuid import uuid4

from pytest_cases import fixture, fixture_union, parametrize

from tests.network.utils import (
    IS_SHARED,
    random_network_all_attr,
    random_network_required_attr,
)

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
def network_create_minimum_data() -> Dict[str, Any]:
    """Dict with Network mandatory attributes."""
    return random_network_required_attr()


@fixture
@parametrize(is_shared=IS_SHARED)
def network_create_data_with_rel(is_shared: bool) -> Dict[str, Any]:
    """Dict with relationships attributes.

    Attribute is_shared has been parametrized.
    """
    return {
        **random_network_all_attr(),
        "is_shared": is_shared,
        "project": None if is_shared else uuid4(),
    }


@fixture
@parametrize("k, v", invalid_create_key_values)
def network_create_invalid_pair(k: str, v: Any) -> Dict[str, Any]:
    """Dict with one invalid key-value pair."""
    return {**random_network_required_attr(), k: v}


@fixture
@parametrize(is_shared=IS_SHARED)
def network_create_invalid_project_conn(is_shared: bool) -> Dict[str, Any]:
    """Invalid project list size.

    Invalid cases: If network is marked as public, the list has at least one element,
    if private, the list has no items.
    """
    return {
        **random_network_required_attr(),
        "is_shared": is_shared,
        "project": None if not is_shared else uuid4(),
    }


network_create_valid_data = fixture_union(
    "network_create_valid_data",
    (network_create_minimum_data, network_create_data_with_rel),
    idstyle="explicit",
)


network_create_invalid_data = fixture_union(
    "network_create_invalid_data",
    (network_create_invalid_pair, network_create_invalid_project_conn),
    idstyle="explicit",
)
