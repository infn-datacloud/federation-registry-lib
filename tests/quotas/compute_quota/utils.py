"""ComputeQuota utilities."""

from typing import Any, Dict

from tests.common.utils import random_bool, random_lower_string, random_non_negative_int


def random_compute_quota_required_attr() -> Dict[str, Any]:
    """Dict with ComputeQuota mandatory attributes."""
    return {}


def random_compute_quota_all_attr() -> Dict[str, Any]:
    """Dict with all ComputeQuota attributes."""
    return {
        **random_compute_quota_required_attr(),
        "description": random_lower_string(),
        "per_user": random_bool(),
        "cores": random_non_negative_int(),
        "instances": random_non_negative_int(),
        "ram": random_non_negative_int(),
    }
