"""Quota custom enumerations."""

from enum import Enum

from fedreg.v1.service.enum import ServiceType


class QuotaType(str, Enum):
    """Possible Quota types."""

    BLOCK_STORAGE = ServiceType.BLOCK_STORAGE.value
    COMPUTE = ServiceType.COMPUTE.value
    IDENTITY = ServiceType.IDENTITY.value
    NETWORK = ServiceType.NETWORK.value
    OBJECT_STORE = ServiceType.OBJECT_STORE.value
    STORAGECLASS = "storageclass"
