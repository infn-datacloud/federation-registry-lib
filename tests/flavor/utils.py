"""Flavor utilities."""
from typing import Any, Dict
from uuid import uuid4

from tests.common.utils import (
    random_bool,
    random_lower_string,
    random_non_negative_int,
    random_positive_int,
)

IS_PUBLIC = [True, False]
GPU_DETAILS = [
    ("gpu_model", random_lower_string()),  # gpus is 0
    ("gpu_vendor", random_lower_string()),  # gpus is 0
]


def random_flavor_required_attr() -> Dict[str, Any]:
    """Return a dict with the Flavor required attributes initialized."""
    return {"name": random_lower_string(), "uuid": uuid4()}


def random_flavor_all_attr() -> Dict[str, Any]:
    """Dict with all Flavor attributes."""
    return {
        **random_flavor_required_attr(),
        "is_public": random_bool(),
        "description": random_lower_string(),
        "disk": random_non_negative_int(),
        "ram": random_non_negative_int(),
        "vcpus": random_non_negative_int(),
        "swap": random_non_negative_int(),
        "ephemeral": random_non_negative_int(),
        "infiniband": random_bool(),
        "gpus": random_positive_int(),
        "gpu_model": random_lower_string(),
        "gpu_vendor": random_lower_string(),
        "local_storage": random_lower_string(),
    }
