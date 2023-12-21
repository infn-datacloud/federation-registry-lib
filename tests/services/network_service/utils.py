"""NetworkService utilitiees."""
from random import choice
from typing import Any, Dict

from app.service.enum import NetworkServiceName
from tests.common.utils import random_lower_string, random_url


def random_network_service_required_attr() -> Dict[str, Any]:
    """Dict with NetworkService mandatory attributes."""
    return {"endpoint": random_url(), "name": random_network_service_name()}


def random_network_service_all_attr() -> Dict[str, Any]:
    """Dict with all NetworkService attributes."""
    return {
        **random_network_service_required_attr(),
        "description": random_lower_string(),
    }


def random_network_service_name() -> str:
    """Return one of the possible NetworkService names."""
    return choice([i.value for i in NetworkServiceName])
