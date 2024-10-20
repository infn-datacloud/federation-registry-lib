"""Provider custom enumerations."""
from enum import Enum


class ProviderStatus(str, Enum):
    """Provider current status."""

    ACTIVE: str = "active"
    MAINTENANCE: str = "maintenance"
    REMOVED: str = "removed"
    LIMITED: str = "limited"


class ProviderType(str, Enum):
    """IaaS type."""

    OS: str = "openstack"
    K8S: str = "kubernetes"
