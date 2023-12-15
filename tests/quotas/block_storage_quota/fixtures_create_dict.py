"""BlockStorageQuota specific fixtures."""
from typing import Any, Dict
from uuid import uuid4

from pytest_cases import fixture, fixture_union, parametrize

from tests.utils.utils import random_bool, random_lower_string, random_non_negative_int

invalid_create_key_values = [
    ("description", None),
    ("per_user", None),
    ("gigabytes", -2),  # -1 is valid
    ("per_volume_gigabytes", -2),  # -1 is valid
    ("volumes", -2),  # -1 is valid
]


@fixture
def block_storage_quota_create_mandatory_data() -> Dict[str, Any]:
    """Dict with BlockStorageQuota mandatory attributes."""
    return {}


@fixture
def block_storage_quota_create_all_data(
    block_storage_quota_create_mandatory_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with all BlockStorageQuota attributes."""
    return {
        **block_storage_quota_create_mandatory_data,
        "description": random_lower_string(),
        "per_user": random_bool(),
        "gigabytes": random_non_negative_int(),
        "per_volume_gigabytes": random_non_negative_int(),
        "volumes": random_non_negative_int(),
    }


@fixture
def block_storage_quota_create_data_with_rel(
    block_storage_quota_create_all_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with relationships attributes."""
    return {**block_storage_quota_create_all_data, "project": uuid4()}


@fixture
@parametrize("k, v", invalid_create_key_values)
def block_storage_quota_create_invalid_pair(
    block_storage_quota_create_data_with_rel: Dict[str, Any], k: str, v: Any
) -> Dict[str, Any]:
    """Dict with one invalid key-value pair."""
    data = {**block_storage_quota_create_data_with_rel}
    data[k] = v
    return data


block_storage_quota_create_valid_data = fixture_union(
    "block_storage_quota_create_valid_data",
    (block_storage_quota_create_data_with_rel,),
    idstyle="explicit",
)


block_storage_quota_create_invalid_data = fixture_union(
    "block_storage_quota_create_invalid_data",
    (
        block_storage_quota_create_all_data,
        block_storage_quota_create_invalid_pair,
    ),
    idstyle="explicit",
)
