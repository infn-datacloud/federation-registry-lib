from enum import Enum


class ProviderStatus(Enum):
    ACTIVE: str = "active"
    MAINTENANCE: str = "maintenance"
    REMOVED: str = "removed"


class ProviderType(Enum):
    OS: str = "openstack"
    K8S: str = "kubernetes"
