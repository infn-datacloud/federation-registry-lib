"""Image utilities."""
from random import choice
from typing import Any, Dict
from uuid import uuid4

from app.image.enum import ImageOS
from tests.common.utils import random_bool, random_lower_string

IS_PUBLIC = [True, False]


def random_image_required_attr() -> Dict[str, Any]:
    """Return a dict with the Image required attributes initialized."""
    return {"name": random_lower_string(), "uuid": uuid4()}


def random_image_all_attr() -> Dict[str, Any]:
    """Dict with all Image attributes."""
    return {
        **random_image_required_attr(),
        "is_public": random_bool(),
        "description": random_lower_string(),
        "os_type": random_os_type(),
        "os_distro": random_lower_string(),
        "os_version": random_lower_string(),
        "architecture": random_lower_string(),
        "kernel_id": random_lower_string(),
        "cuda_support": random_bool(),
        "gpu_driver": random_bool(),
        "tags": [random_lower_string()],
    }


def random_image_required_rel(is_public: bool) -> Dict[str, Any]:
    """Return a dict with the Image required attributes initialized."""
    return {"projects": [] if is_public else [uuid4()]}


def random_os_type() -> str:
    """Return one of the possible image OS values."""
    return choice([i.value for i in ImageOS])
