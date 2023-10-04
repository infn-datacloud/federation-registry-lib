import copy

import pytest
from app.service.enum import ServiceName, ServiceType
from app.tests.utils.service import (
    create_random_block_storage_service,
    create_random_compute_service,
    create_random_identity_service,
    create_random_network_service,
)
from pydantic import ValidationError


def test_create_schema():
    create_random_block_storage_service()
    create_random_block_storage_service(default=True)
    create_random_block_storage_service(with_quotas=True)
    item = create_random_block_storage_service(default=True, with_quotas=True)

    q1 = item.quotas[0]
    q2 = copy.deepcopy(q1)
    q2.per_user = not q1.per_user
    item.quotas = [q1, q2]

    create_random_compute_service()
    create_random_compute_service(default=True)
    create_random_compute_service(with_quotas=True)
    create_random_compute_service(default=True, with_quotas=True)
    create_random_compute_service(with_flavors=True)
    create_random_compute_service(default=True, with_flavors=True)
    create_random_compute_service(with_images=True)
    create_random_compute_service(default=True, with_images=True)
    item = create_random_compute_service(
        with_flavors=True, with_images=True, with_quotas=True
    )

    q1 = item.quotas[0]
    q2 = copy.deepcopy(q1)
    q2.per_user = not q1.per_user
    item.quotas = [q1, q2]

    create_random_identity_service()
    create_random_identity_service(default=True)

    create_random_network_service()
    create_random_network_service(default=True)
    create_random_network_service(with_networks=True)
    create_random_network_service(default=True, with_networks=True)


def test_invalid_create_schema():
    a = create_random_block_storage_service(with_quotas=True)
    with pytest.raises(ValidationError):
        a.type = ServiceType.COMPUTE.value
    with pytest.raises(ValidationError):
        a.type = ServiceType.IDENTITY.value
    with pytest.raises(ValidationError):
        a.type = ServiceType.NETWORK.value
    with pytest.raises(ValidationError):
        a.name = ServiceName.OPENSTACK_KEYSTONE.value
    with pytest.raises(ValidationError):
        a.name = ServiceName.OPENSTACK_NEUTRON.value
    with pytest.raises(ValidationError):
        a.name = ServiceName.OPENSTACK_NOVA.value
    with pytest.raises(ValidationError):
        a.endpoint = None
    with pytest.raises(ValidationError):
        a.quotas = [a.quotas[0], a.quotas[0]]

    a = create_random_compute_service(
        with_flavors=True, with_images=True, with_quotas=True
    )
    with pytest.raises(ValidationError):
        a.type = ServiceType.BLOCK_STORAGE.value
    with pytest.raises(ValidationError):
        a.type = ServiceType.IDENTITY.value
    with pytest.raises(ValidationError):
        a.type = ServiceType.NETWORK.value
    with pytest.raises(ValidationError):
        a.name = ServiceName.OPENSTACK_CINDER.value
    with pytest.raises(ValidationError):
        a.name = ServiceName.OPENSTACK_KEYSTONE.value
    with pytest.raises(ValidationError):
        a.name = ServiceName.OPENSTACK_NEUTRON.value
    with pytest.raises(ValidationError):
        a.endpoint = None
    with pytest.raises(ValidationError):
        a.flavors = [a.flavors[0], a.flavors[0]]
    with pytest.raises(ValidationError):
        a.images = [a.images[0], a.images[0]]
    with pytest.raises(ValidationError):
        a.quotas = [a.quotas[0], a.quotas[0]]

    a = create_random_identity_service()
    with pytest.raises(ValidationError):
        a.type = ServiceType.BLOCK_STORAGE.value
    with pytest.raises(ValidationError):
        a.type = ServiceType.COMPUTE.value
    with pytest.raises(ValidationError):
        a.type = ServiceType.NETWORK.value
    with pytest.raises(ValidationError):
        a.name = ServiceName.OPENSTACK_CINDER.value
    with pytest.raises(ValidationError):
        a.name = ServiceName.OPENSTACK_NEUTRON.value
    with pytest.raises(ValidationError):
        a.name = ServiceName.OPENSTACK_NOVA.value
    with pytest.raises(ValidationError):
        a.endpoint = None

    a = create_random_network_service(with_networks=True)
    with pytest.raises(ValidationError):
        a.type = ServiceType.BLOCK_STORAGE.value
    with pytest.raises(ValidationError):
        a.type = ServiceType.COMPUTE.value
    with pytest.raises(ValidationError):
        a.type = ServiceType.IDENTITY.value
    with pytest.raises(ValidationError):
        a.name = ServiceName.OPENSTACK_CINDER.value
    with pytest.raises(ValidationError):
        a.name = ServiceName.OPENSTACK_KEYSTONE.value
    with pytest.raises(ValidationError):
        a.name = ServiceName.OPENSTACK_NOVA.value
    with pytest.raises(ValidationError):
        a.endpoint = None
    with pytest.raises(ValidationError):
        a.networks = [a.networks[0], a.networks[0]]
