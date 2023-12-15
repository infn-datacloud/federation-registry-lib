"""BlockStorageQuota specific fixtures."""
from typing import Any, Dict

from pytest_cases import fixture, parametrize

from app.quota.enum import QuotaType
from tests.utils.utils import random_bool, random_lower_string, random_non_negative_int

patch_key_values = {
    ("description", random_lower_string()),
    ("per_user", random_bool()),
    ("gigabytes", random_non_negative_int()),
    ("gigabytes", -1),
    ("per_volume_gigabytes", random_non_negative_int()),
    ("per_volume_gigabytes", -1),
    ("volumes", random_non_negative_int()),
    ("volumes", -1),
}
invalid_patch_key_values = {  # None is not accepted because there is a default
    ("description", None),
    ("per_user", None),
    ("type", QuotaType.COMPUTE),
    ("type", QuotaType.NETWORK),
    ("gigabytes", -2),  # -1 is valid
    ("per_volume_gigabytes", -2),  # -1 is valid
    ("volumes", -2),  # -1 is valid
}


@fixture
@parametrize("k, v", patch_key_values)
def block_storage_quota_patch_valid_data(k: str, v: Any) -> Dict[str, Any]:
    """Valid set of single key-value pair for a BlockStorageQuota patch schema."""
    return {k: v}


@fixture
@parametrize("k, v", invalid_patch_key_values)
def block_storage_quota_patch_invalid_data(k: str, v: Any) -> Dict[str, Any]:
    """Invalid set of attributes for a BlockStorageQuota patch schema."""
    return {k: v}
