"""Network specific fixtures."""
from typing import Any, Dict
from uuid import uuid4

from pytest_cases import fixture, fixture_union, parametrize

from tests.utils.utils import random_bool, random_lower_string, random_non_negative_int

patch_key_values = {
    ("description", random_lower_string()),
    ("uuid", uuid4()),
    ("name", random_lower_string()),
    ("is_router_external", random_bool()),
    ("is_default", random_bool()),
    ("mtu", random_non_negative_int()),
    ("proxy_ip", random_lower_string()),
    ("proxy_user", random_lower_string()),
}
invalid_patch_key_values = {  # None is not accepted because there is a default
    ("description", None),
    ("is_shared", None),
    ("is_router_external", None),
    ("is_default", None),
    ("mtu", 0),
    ("tags", None),
}


@fixture
@parametrize("k, v", patch_key_values)
def network_patch_valid_data_single_attr(k: str, v: Any) -> Dict[str, Any]:
    """Valid set of single key-value pair for a Network patch schema."""
    return {k: v}


@fixture
def network_patch_valid_data_for_tags() -> Dict[str, Any]:
    """Valid set of attributes for a Network patch schema. Tags details."""
    return {"tags": [random_lower_string()]}


network_patch_valid_data = fixture_union(
    "network_patch_valid_data",
    (network_patch_valid_data_single_attr, network_patch_valid_data_for_tags),
    idstyle="explicit",
)


@fixture
@parametrize("k, v", invalid_patch_key_values)
def network_patch_invalid_data(k: str, v: Any) -> Dict[str, Any]:
    """Invalid set of attributes for a Network patch schema."""
    return {k: v}
