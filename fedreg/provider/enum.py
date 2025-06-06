"""Provider custom enumerations."""

from enum import Enum


class ProviderType(str, Enum):
    """IaaS type."""

    OS: str = "openstack"
    K8S: str = "kubernetes"
