"""BlockStorageQuota specific fixtures."""
from typing import Any, Dict
from uuid import uuid4

from pytest_cases import fixture, fixture_union, parametrize

from tests.quotas.block_storage_quota.utils import (
    random_block_storage_quota_all_attr,
    random_block_storage_quota_required_attr,
)

invalid_create_key_values = [
    ("description", None),
    ("per_user", None),
    ("gigabytes", -2),  # -1 is valid
    ("per_volume_gigabytes", -2),  # -1 is valid
    ("volumes", -2),  # -1 is valid
]


@fixture
def block_storage_quota_create_minimum_data() -> Dict[str, Any]:
    """Dict with BlockStorageQuota mandatory attributes."""
    return random_block_storage_quota_required_attr()


@fixture
def block_storage_quota_create_data_with_rel() -> Dict[str, Any]:
    """Dict with relationships attributes."""
    return {**random_block_storage_quota_all_attr(), "project": uuid4()}


@fixture
@parametrize("k, v", invalid_create_key_values)
def block_storage_quota_create_invalid_pair(
    block_storage_quota_create_data_with_rel: Dict[str, Any], k: str, v: Any
) -> Dict[str, Any]:
    """Dict with one invalid key-value pair."""
    return {**block_storage_quota_create_data_with_rel, k: v}


block_storage_quota_create_valid_data = fixture_union(
    "block_storage_quota_create_valid_data",
    (block_storage_quota_create_data_with_rel,),
    idstyle="explicit",
)


block_storage_quota_create_invalid_data = fixture_union(
    "block_storage_quota_create_invalid_data",
    (
        block_storage_quota_create_minimum_data,
        block_storage_quota_create_invalid_pair,
    ),
    idstyle="explicit",
)
