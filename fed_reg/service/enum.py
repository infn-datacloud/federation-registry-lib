"""Service custom enumerations."""
from enum import Enum


class BlockStorageServiceName(str, Enum):
    """Possible IaaS block storage services names."""

    OPENSTACK_CINDER: str = "org.openstack.cinder"


class ComputeServiceName(str, Enum):
    """Possible IaaS compute services names."""

    OPENSTACK_NOVA: str = "org.openstack.nova"


class IdentityServiceName(str, Enum):
    """Possible IaaS identity services names."""

    OPENSTACK_KEYSTONE: str = "org.openstack.keystone"


class NetworkServiceName(str, Enum):
    """Possible IaaS network services names."""

    OPENSTACK_NEUTRON: str = "org.openstack.neutron"


class ObjectStorageServiceName(str, Enum):
    """Possible IaaS object storage services names."""

    OPENSTACK_SWIFT: str = "org.openstack.swift"


class ServiceType(str, Enum):
    """Possible IaaS services types."""

    BLOCK_STORAGE: str = "block-storage"
    COMPUTE: str = "compute"
    IDENTITY: str = "identity"
    NETWORK: str = "network"
    OBJECT_STORAGE: str = "object-storage"
