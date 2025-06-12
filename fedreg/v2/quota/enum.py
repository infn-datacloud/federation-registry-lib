"""Quota enumerations"""

from enum import Enum

from fedreg.v2.service.enum import ServiceType


class QuotaType(str, Enum):
    """Possible Quota types."""

    BLOCK_STORAGE = ServiceType.BLOCK_STORAGE.value
    COMPUTE = ServiceType.COMPUTE.value
    NETWORKING = ServiceType.NETWORKING.value
    OBJECT_STORE = ServiceType.OBJECT_STORE.value
    STORAGECLASS = "storageclass"
