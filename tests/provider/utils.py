"""Provider utilities."""
from random import choice
from typing import Any, Dict

from app.provider.enum import ProviderStatus, ProviderType
from tests.common.utils import random_bool, random_email, random_lower_string


def random_provider_required_attr() -> Dict[str, Any]:
    """Return a dict with the Provider required attributes initialized."""
    return {"name": random_lower_string(), "type": random_type()}


def random_provider_all_attr() -> Dict[str, Any]:
    """Dict with all Provider attributes."""
    return {
        **random_provider_required_attr(),
        "description": random_lower_string(),
        "status": random_status(),
        "is_public": random_bool(),
        "support_emails": [random_email()],
    }


def random_status() -> str:
    """Return one of the possible provider status values."""
    return choice([i.value for i in ProviderStatus])


def random_type() -> str:
    """Return one of the possible provider types."""
    return choice([i.value for i in ProviderType])
