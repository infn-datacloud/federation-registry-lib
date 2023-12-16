"""Provider utilities."""
from random import choice

from app.provider.enum import ProviderStatus, ProviderType


def random_status() -> str:
    """Return one of the possible provider status values."""
    return choice([i.value for i in ProviderStatus])


def random_type() -> str:
    """Return one of the possible provider types."""
    return choice([i.value for i in ProviderType])
