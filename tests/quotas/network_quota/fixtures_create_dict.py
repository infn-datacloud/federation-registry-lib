"""NetworkQuota specific fixtures."""
from typing import Any, Dict
from uuid import uuid4

from pytest_cases import fixture, fixture_union, parametrize

from tests.common.utils import random_bool, random_lower_string, random_non_negative_int

invalid_create_key_values = [
    ("description", None),
    ("per_user", None),
    ("public_ips", -2),  # -1 is valid
    ("networks", -2),  # -1 is valid
    ("ports", -2),  # -1 is valid
    ("security_groups", -2),  # -1 is valid
    ("security_group_rules", -2),  # -1 is valid
]


@fixture
def network_quota_create_mandatory_data() -> Dict[str, Any]:
    """Dict with NetworkQuota mandatory attributes."""
    return {}


@fixture
def network_quota_create_all_data(
    network_quota_create_mandatory_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with all NetworkQuota attributes."""
    return {
        **network_quota_create_mandatory_data,
        "description": random_lower_string(),
        "per_user": random_bool(),
        "public_ips": random_non_negative_int(),
        "networks": random_non_negative_int(),
        "ports": random_non_negative_int(),
        "security_groups": random_non_negative_int(),
        "security_group_rules": random_non_negative_int(),
    }


@fixture
def network_quota_create_data_with_rel(
    network_quota_create_all_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with relationships attributes."""
    return {**network_quota_create_all_data, "project": uuid4()}


@fixture
@parametrize("k, v", invalid_create_key_values)
def network_quota_create_invalid_pair(
    network_quota_create_data_with_rel: Dict[str, Any], k: str, v: Any
) -> Dict[str, Any]:
    """Dict with one invalid key-value pair."""
    return {**network_quota_create_data_with_rel, k: v}


network_quota_create_valid_data = fixture_union(
    "network_quota_create_valid_data",
    (network_quota_create_data_with_rel,),
    idstyle="explicit",
)


network_quota_create_invalid_data = fixture_union(
    "network_quota_create_invalid_data",
    (
        network_quota_create_all_data,
        network_quota_create_invalid_pair,
    ),
    idstyle="explicit",
)
