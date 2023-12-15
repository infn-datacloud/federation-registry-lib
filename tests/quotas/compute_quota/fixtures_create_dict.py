"""ComputeQuota specific fixtures."""
from typing import Any, Dict
from uuid import uuid4

from pytest_cases import fixture, fixture_union, parametrize

from tests.utils.utils import random_bool, random_lower_string, random_non_negative_int

invalid_create_key_values = [
    ("description", None),
    ("per_user", None),
    ("cores", -1),
    ("instances", -1),
    ("ram", -1),
]


@fixture
def compute_quota_create_mandatory_data() -> Dict[str, Any]:
    """Dict with ComputeQuota mandatory attributes."""
    return {}


@fixture
def compute_quota_create_all_data(
    compute_quota_create_mandatory_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with all ComputeQuota attributes."""
    return {
        **compute_quota_create_mandatory_data,
        "description": random_lower_string(),
        "per_user": random_bool(),
        "cores": random_non_negative_int(),
        "instances": random_non_negative_int(),
        "ram": random_non_negative_int(),
    }


@fixture
def compute_quota_create_data_with_rel(
    compute_quota_create_all_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with relationships attributes."""
    return {**compute_quota_create_all_data, "project": uuid4()}


@fixture
@parametrize("k, v", invalid_create_key_values)
def compute_quota_create_invalid_pair(
    compute_quota_create_data_with_rel: Dict[str, Any], k: str, v: Any
) -> Dict[str, Any]:
    """Dict with one invalid key-value pair."""
    return {**compute_quota_create_data_with_rel, k: v}


compute_quota_create_valid_data = fixture_union(
    "compute_quota_create_valid_data",
    (compute_quota_create_data_with_rel,),
    idstyle="explicit",
)


compute_quota_create_invalid_data = fixture_union(
    "compute_quota_create_invalid_data",
    (
        compute_quota_create_all_data,
        compute_quota_create_invalid_pair,
    ),
    idstyle="explicit",
)
