from enum import Enum


class ServiceName(Enum):
    """Possible IaaS services names."""

    OPENSTACK_NOVA: str = "org.openstack.nova"
    OPENSTACK_CINDER: str = "org.openstack.cinder"
    OPENSTACK_KEYSTONE: str = "org.openstack.keystone"
    OPENSTACK_NEUTRON: str = "org.openstack.neutron"


class ServiceType(Enum):
    """Possible IaaS services types."""

    BLOCK_STORAGE: str = "block-storage"
    COMPUTE: str = "compute"
    IDENTITY: str = "identity"
    NETWORK: str = "network"
