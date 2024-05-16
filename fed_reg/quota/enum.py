"""Quota custom enumerations."""
from enum import Enum


class QuotaType(str, Enum):
    """Possible Quota types."""

    BLOCK_STORAGE: str = "block-storage"
    COMPUTE: str = "compute"
    NETWORK: str = "network"
    OBJECT_STORAGE: str = "object-storage"
