"""Quota custom enumerations."""

from fedreg.v1.service.enum import ServiceType


class QuotaType(ServiceType):
    """Possible Quota types."""

    STORAGECLASS = "storageclass"
