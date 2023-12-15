"""NetworkQuota specific fixtures."""
from typing import Any, Dict

from pytest_cases import fixture, parametrize

from app.quota.enum import QuotaType
from tests.utils.utils import random_bool, random_lower_string, random_non_negative_int

patch_key_values = [
    ("description", random_lower_string()),
    ("per_user", random_bool()),
    ("public_ips", random_non_negative_int()),
    ("public_ips", -1),
    ("networks", random_non_negative_int()),
    ("networks", -1),
    ("ports", random_non_negative_int()),
    ("ports", -1),
    ("security_groups", random_non_negative_int()),
    ("security_groups", -1),
    ("security_group_rules", random_non_negative_int()),
    ("security_group_rules", -1),
]
invalid_patch_key_values = [  # None is not accepted because there is a default
    ("description", None),
    ("per_user", None),
    ("type", QuotaType.BLOCK_STORAGE),
    ("type", QuotaType.COMPUTE),
    ("public_ips", -2),  # -1 is valid
    ("networks", -2),  # -1 is valid
    ("ports", -2),  # -1 is valid
    ("security_groups", -2),  # -1 is valid
    ("security_group_rules", -2),  # -1 is valid
]


@fixture
@parametrize("k, v", patch_key_values)
def network_quota_patch_valid_data(k: str, v: Any) -> Dict[str, Any]:
    """Valid set of single key-value pair for a NetworkQuota patch schema."""
    return {k: v}


@fixture
@parametrize("k, v", invalid_patch_key_values)
def network_quota_patch_invalid_data(k: str, v: Any) -> Dict[str, Any]:
    """Invalid set of attributes for a NetworkQuota patch schema."""
    return {k: v}
