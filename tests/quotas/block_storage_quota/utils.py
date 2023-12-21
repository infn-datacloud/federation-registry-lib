"""BlockStorageQuota utilities."""
from typing import Any, Dict
from uuid import uuid4

from tests.common.utils import random_bool, random_lower_string, random_non_negative_int


def random_block_storage_quota_required_attr() -> Dict[str, Any]:
    """Dict with BlockStorageQuota mandatory attributes."""
    return {}


def random_block_storage_quota_all_attr() -> Dict[str, Any]:
    """Dict with all BlockStorageQuota attributes."""
    return {
        **random_block_storage_quota_required_attr(),
        "description": random_lower_string(),
        "per_user": random_bool(),
        "gigabytes": random_non_negative_int(),
        "per_volume_gigabytes": random_non_negative_int(),
        "volumes": random_non_negative_int(),
    }


def random_block_storage_quota_required_rel() -> Dict[str, Any]:
    """Dict with all BlockStorageQuota relationships."""
    return {"project": uuid4()}
