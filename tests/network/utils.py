"""Network utilities."""
from typing import Any, Dict
from uuid import uuid4

from tests.common.utils import random_bool, random_lower_string, random_positive_int

IS_SHARED = [True, False]


def random_network_required_attr() -> Dict[str, Any]:
    """Return a dict with the Network required attributes initialized."""
    return {"name": random_lower_string(), "uuid": uuid4()}


def random_network_all_attr() -> Dict[str, Any]:
    """Dict with all Network attributes."""
    return {
        **random_network_required_attr(),
        "is_shared": random_bool(),
        "description": random_lower_string(),
        "is_router_external": random_bool(),
        "is_default": random_bool(),
        "mtu": random_positive_int(),
        "proxy_ip": random_lower_string(),
        "proxy_user": random_lower_string(),
        "tags": [random_lower_string()],
    }


def random_network_required_rel(is_shared: bool) -> Dict[str, Any]:
    """Return a dict with the Network required attributes initialized."""
    return {"project": None if is_shared else uuid4()}
