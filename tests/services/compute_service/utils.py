"""ComputeService utilitiees."""
from random import choice
from typing import Any, Dict

from app.service.enum import ComputeServiceName
from tests.common.utils import random_lower_string, random_url


def random_compute_service_required_attr() -> Dict[str, Any]:
    """Dict with ComputeService mandatory attributes."""
    return {"endpoint": random_url(), "name": random_compute_service_name()}


def random_compute_service_all_attr() -> Dict[str, Any]:
    """Dict with all ComputeService attributes."""
    return {
        **random_compute_service_required_attr(),
        "description": random_lower_string(),
    }


def random_compute_service_name() -> str:
    """Return one of the possible ComputeService names."""
    return choice([i.value for i in ComputeServiceName])
