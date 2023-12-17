"""ComputeQuota specific fixtures."""
from typing import Any, Dict
from uuid import uuid4

from pytest_cases import fixture, fixture_union, parametrize

from tests.quotas.compute_quota.utils import (
    random_compute_quota_all_attr,
    random_compute_quota_required_attr,
)

invalid_create_key_values = [
    ("description", None),
    ("per_user", None),
    ("cores", -1),
    ("instances", -1),
    ("ram", -1),
]


@fixture
def compute_quota_create_minimum_data() -> Dict[str, Any]:
    """Dict with ComputeQuota mandatory attributes."""
    return random_compute_quota_required_attr()


@fixture
def compute_quota_create_data_with_rel() -> Dict[str, Any]:
    """Dict with relationships attributes."""
    return {**random_compute_quota_all_attr(), "project": uuid4()}


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
        compute_quota_create_minimum_data,
        compute_quota_create_invalid_pair,
    ),
    idstyle="explicit",
)
