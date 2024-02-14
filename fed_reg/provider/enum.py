"""Provider custom enumerations."""
from enum import Enum


class ProviderStatus(Enum):
    """Provider current status."""

    ACTIVE: str = "active"
    MAINTENANCE: str = "maintenance"
    REMOVED: str = "removed"


class ProviderType(Enum):
    """IaaS type."""

    OS: str = "openstack"
    K8S: str = "kubernetes"
