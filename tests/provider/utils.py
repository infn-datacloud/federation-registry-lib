"""Provider utilities."""
from random import choice
from typing import Any, Dict

from app.provider.enum import ProviderStatus, ProviderType
from app.provider.schemas import ProviderBase
from tests.common.utils import random_bool, random_email, random_lower_string
from tests.identity_provider.utils import (
    random_identity_provider_required_attr,
    random_identity_provider_required_rel,
)


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


def random_provider_all_no_default_attr() -> Dict[str, Any]:
    """Dict with the provider base attribute different from the default one."""
    data = random_provider_all_attr()
    for k, v in ProviderBase.__fields__.items():
        default = v.get_default()
        if isinstance(default, ProviderStatus) or isinstance(default, ProviderType):
            default = default.value
        while data[k] == default:
            if v.type_ == bool:
                data[k] = random_bool()
            elif v.type_ == ProviderStatus:
                data[k] = random_status()
            elif v.type_ == ProviderType:
                data[k] = random_type()
    return data


def random_provider_required_rel() -> Dict[str, Any]:
    """Return a dict with the Provider required relationships initialized."""
    return {
        "identity_providers": [
            {
                **random_identity_provider_required_attr(),
                **random_identity_provider_required_rel(),
            }
        ]
    }


def random_status() -> str:
    """Return one of the possible provider status values."""
    return choice([i.value for i in ProviderStatus])


def random_type() -> str:
    """Return one of the possible provider types."""
    return choice([i.value for i in ProviderType])
