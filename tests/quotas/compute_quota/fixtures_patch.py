"""ComputeQuota specific fixtures."""
from typing import Any, Dict

from pytest_cases import fixture, parametrize

from app.quota.enum import QuotaType
from tests.utils.utils import random_bool, random_lower_string, random_non_negative_int

patch_key_values = [
    ("description", random_lower_string()),
    ("per_user", random_bool()),
    ("cores", random_non_negative_int()),
    ("instances", random_non_negative_int()),
    ("ram", random_non_negative_int()),
]
invalid_patch_key_values = [  # None is not accepted because there is a default
    ("description", None),
    ("per_user", None),
    ("type", QuotaType.BLOCK_STORAGE),
    ("type", QuotaType.NETWORK),
    ("cores", -1),
    ("instances", -1),
    ("ram", -1),
]


@fixture
@parametrize("k, v", patch_key_values)
def compute_quota_patch_valid_data(k: str, v: Any) -> Dict[str, Any]:
    """Valid set of single key-value pair for a ComputeQuota patch schema."""
    return {k: v}


@fixture
@parametrize("k, v", invalid_patch_key_values)
def compute_quota_patch_invalid_data(k: str, v: Any) -> Dict[str, Any]:
    """Invalid set of attributes for a ComputeQuota patch schema."""
    return {k: v}
