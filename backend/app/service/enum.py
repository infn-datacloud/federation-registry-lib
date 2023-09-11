from enum import Enum


class ServiceName(Enum):
    """Possible IaaS services names."""

    OPENSTACK_NOVA: str = "org.openstack.nova"
    OPENSTACK_CINDER: str = "org.openstack.cinder"
    OPENSTACK_KEYSTONE: str = "org.openstack.keystone"


class ServiceType(Enum):
    """Possible IaaS services types."""

    IDENTITY: str = "identity"
    COMPUTE: str = "compute"
    BLOCK_STORAGE: str = "block-storage"
