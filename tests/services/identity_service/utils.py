"""IdentityService utilitiees."""
from random import choice
from typing import Any, Dict

from app.service.enum import IdentityServiceName
from tests.common.utils import random_lower_string, random_url


def random_identity_service_required_attr() -> Dict[str, Any]:
    """Dict with IdentityService mandatory attributes."""
    return {"endpoint": random_url(), "name": random_identity_service_name()}


def random_identity_service_all_attr() -> Dict[str, Any]:
    """Dict with all IdentityService attributes."""
    return {
        **random_identity_service_required_attr(),
        "description": random_lower_string(),
    }


def random_identity_service_name() -> str:
    """Return one of the possible IdentityService names."""
    return choice([i.value for i in IdentityServiceName])
