"""Service custom enumerations."""

from enum import Enum


class BlockStorageServiceName(str, Enum):
    """Possible IaaS block storage services names."""

    OPENSTACK_CINDER = "org.openstack.cinder"
    KUBERNETES = "storage.k8s.io/v1"


class ComputeServiceName(str, Enum):
    """Possible IaaS compute services names."""

    OPENSTACK_NOVA = "org.openstack.nova"
    KUBERNETES = "v1"


class IdentityServiceName(str, Enum):
    """Possible IaaS identity services names."""

    OPENSTACK_KEYSTONE = "org.openstack.keystone"
    KUBERNETES = "v1"


class NetworkServiceName(str, Enum):
    """Possible IaaS network services names."""

    OPENSTACK_NEUTRON = "org.openstack.neutron"


class ObjectStoreServiceName(str, Enum):
    """Possible IaaS object storage services names."""

    OPENSTACK_SWIFT = "org.openstack.swift"
    OPENSTACK_SWIFT_S3 = "org.openstack.swift-s3"


class ServiceType(str, Enum):
    """Possible IaaS services types."""

    BLOCK_STORAGE = "block-storage"
    COMPUTE = "compute"
    IDENTITY = "identity"
    NETWORK = "network"
    OBJECT_STORE = "object-store"
