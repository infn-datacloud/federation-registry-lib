from enum import Enum


class BlockStorageServiceName(Enum):
    """Possible IaaS block storage services names."""

    OPENSTACK_CINDER: str = "org.openstack.cinder"


class ComputeServiceName(Enum):
    """Possible IaaS compute services names."""

    OPENSTACK_NOVA: str = "org.openstack.nova"


class IdentityServiceName(Enum):
    """Possible IaaS identity services names."""

    OPENSTACK_KEYSTONE: str = "org.openstack.keystone"


class NetworkServiceName(Enum):
    """Possible IaaS network services names."""

    OPENSTACK_NEUTRON: str = "org.openstack.neutron"


class ServiceType(Enum):
    """Possible IaaS services types."""

    BLOCK_STORAGE: str = "block-storage"
    COMPUTE: str = "compute"
    IDENTITY: str = "identity"
    NETWORK: str = "network"
