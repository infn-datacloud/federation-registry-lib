"""NetworkQuota utilities."""
from typing import Any, Dict
from uuid import uuid4

from tests.common.utils import random_bool, random_lower_string, random_non_negative_int


def random_network_quota_required_attr() -> Dict[str, Any]:
    """Dict with NetworkQuota mandatory attributes."""
    return {}


def random_network_quota_all_attr() -> Dict[str, Any]:
    """Dict with all NetworkQuota attributes."""
    return {
        **random_network_quota_required_attr(),
        "description": random_lower_string(),
        "per_user": random_bool(),
        "public_ips": random_non_negative_int(),
        "networks": random_non_negative_int(),
        "ports": random_non_negative_int(),
        "security_groups": random_non_negative_int(),
        "security_group_rules": random_non_negative_int(),
    }


def random_network_quota_required_rel() -> Dict[str, Any]:
    """Dict with all NetworkQuota relationships."""
    return {"project": uuid4()}
