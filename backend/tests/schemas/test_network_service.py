from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.service.enum import (
    BlockStorageServiceName,
    ComputeServiceName,
    IdentityServiceName,
    ServiceType,
)
from app.service.models import NetworkService
from app.service.schemas import (
    NetworkServiceRead,
    NetworkServiceReadPublic,
    NetworkServiceReadShort,
)
from app.service.schemas_extended import (
    NetworkServiceReadExtended,
    NetworkServiceReadExtendedPublic,
)
from tests.utils.network_service import (
    create_random_network_service,
    validate_read_extended_network_service_attrs,
    validate_read_extended_public_network_service_attrs,
    validate_read_network_service_attrs,
    validate_read_public_network_service_attrs,
    validate_read_short_network_service_attrs,
)
from tests.utils.utils import random_lower_string


def test_create_schema():
    """Create a valid 'Create' Schema."""
    create_random_network_service()
    create_random_network_service(default=True)
    create_random_network_service(with_networks=True)
    create_random_network_service(default=True, with_networks=True)
    create_random_network_service(with_networks=True, projects=[uuid4()])
    create_random_network_service(default=True, with_networks=True, projects=[uuid4()])


def test_invalid_create_schema():
    """List all invalid situations for a 'Create' Schema."""
    a = create_random_network_service(with_networks=True, projects=[uuid4()])
    with pytest.raises(ValidationError):
        a.type = ServiceType.BLOCK_STORAGE.value
    with pytest.raises(ValidationError):
        a.type = ServiceType.COMPUTE.value
    with pytest.raises(ValidationError):
        a.type = ServiceType.IDENTITY.value
    with pytest.raises(ValidationError):
        a.type = random_lower_string()
    with pytest.raises(ValidationError):
        a.name = BlockStorageServiceName.OPENSTACK_CINDER.value
    with pytest.raises(ValidationError):
        a.name = ComputeServiceName.OPENSTACK_NOVA.value
    with pytest.raises(ValidationError):
        a.name = IdentityServiceName.OPENSTACK_KEYSTONE.value
    with pytest.raises(ValidationError):
        a.name = random_lower_string()
    with pytest.raises(ValidationError):
        a.endpoint = None
    with pytest.raises(ValidationError):
        # Duplicated networks
        a.networks = [a.networks[0], a.networks[0]]
    with pytest.raises(ValidationError):
        # Duplicated quotas
        a.quotas = [a.quotas[0], a.quotas[0]]


def test_read_schema(db_network_serv: NetworkService):
    """Create a valid 'Read' Schema from DB object.

    Apply conversion for this item for all read schemas. No one of them should raise
    errors.

    Target service is linked only to the parent region.
    """
    schema = NetworkServiceRead.from_orm(db_network_serv)
    validate_read_network_service_attrs(obj_out=schema, db_item=db_network_serv)
    schema = NetworkServiceReadShort.from_orm(db_network_serv)
    validate_read_short_network_service_attrs(obj_out=schema, db_item=db_network_serv)
    schema = NetworkServiceReadPublic.from_orm(db_network_serv)
    validate_read_public_network_service_attrs(obj_out=schema, db_item=db_network_serv)
    schema = NetworkServiceReadExtended.from_orm(db_network_serv)
    validate_read_extended_network_service_attrs(
        obj_out=schema, db_item=db_network_serv
    )
    schema = NetworkServiceReadExtendedPublic.from_orm(db_network_serv)
    validate_read_extended_public_network_service_attrs(
        obj_out=schema, db_item=db_network_serv
    )


def test_read_schema_with_single_network(
    db_network_serv_with_single_network: NetworkService,
):
    """Create a valid 'Read' Schema from DB object.

    Apply conversion for this item for all read schemas. No one of them should raise
    errors.

    Target service is linked only to one network.
    """
    schema = NetworkServiceRead.from_orm(db_network_serv_with_single_network)
    validate_read_network_service_attrs(
        obj_out=schema, db_item=db_network_serv_with_single_network
    )
    schema = NetworkServiceReadShort.from_orm(db_network_serv_with_single_network)
    validate_read_short_network_service_attrs(
        obj_out=schema, db_item=db_network_serv_with_single_network
    )
    schema = NetworkServiceReadPublic.from_orm(db_network_serv_with_single_network)
    validate_read_public_network_service_attrs(
        obj_out=schema, db_item=db_network_serv_with_single_network
    )
    schema = NetworkServiceReadExtended.from_orm(db_network_serv_with_single_network)
    validate_read_extended_network_service_attrs(
        obj_out=schema, db_item=db_network_serv_with_single_network
    )
    schema = NetworkServiceReadExtendedPublic.from_orm(
        db_network_serv_with_single_network
    )
    validate_read_extended_public_network_service_attrs(
        obj_out=schema, db_item=db_network_serv_with_single_network
    )


def test_read_schema_with_multiple_networks(
    db_network_serv_with_multiple_networks: NetworkService,
):
    """Create a valid 'Read' Schema from DB object.

    Apply conversion for this item for all read schemas. No one of them should raise
    errors.

    Target service is linked multiple networks.
    """
    schema = NetworkServiceRead.from_orm(db_network_serv_with_multiple_networks)
    validate_read_network_service_attrs(
        obj_out=schema, db_item=db_network_serv_with_multiple_networks
    )
    schema = NetworkServiceReadShort.from_orm(db_network_serv_with_multiple_networks)
    validate_read_short_network_service_attrs(
        obj_out=schema, db_item=db_network_serv_with_multiple_networks
    )
    schema = NetworkServiceReadPublic.from_orm(db_network_serv_with_multiple_networks)
    validate_read_public_network_service_attrs(
        obj_out=schema, db_item=db_network_serv_with_multiple_networks
    )
    schema = NetworkServiceReadExtended.from_orm(db_network_serv_with_multiple_networks)
    assert len(schema.networks) > 1
    validate_read_extended_network_service_attrs(
        obj_out=schema, db_item=db_network_serv_with_multiple_networks
    )
    schema = NetworkServiceReadExtendedPublic.from_orm(
        db_network_serv_with_multiple_networks
    )
    assert len(schema.networks) > 1
    validate_read_extended_public_network_service_attrs(
        obj_out=schema, db_item=db_network_serv_with_multiple_networks
    )


def test_read_schema_with_single_quota(
    db_network_serv_with_single_quota: NetworkService,
):
    """Create a valid 'Read' Schema from DB object.

    Apply conversion for this item for all read schemas. No one of them should raise
    errors.

    Target service is linked only to one block storage quota.
    """
    schema = NetworkServiceRead.from_orm(db_network_serv_with_single_quota)
    validate_read_network_service_attrs(
        obj_out=schema, db_item=db_network_serv_with_single_quota
    )
    schema = NetworkServiceReadShort.from_orm(db_network_serv_with_single_quota)
    validate_read_short_network_service_attrs(
        obj_out=schema, db_item=db_network_serv_with_single_quota
    )
    schema = NetworkServiceReadPublic.from_orm(db_network_serv_with_single_quota)
    validate_read_public_network_service_attrs(
        obj_out=schema, db_item=db_network_serv_with_single_quota
    )
    schema = NetworkServiceReadExtended.from_orm(db_network_serv_with_single_quota)
    validate_read_extended_network_service_attrs(
        obj_out=schema, db_item=db_network_serv_with_single_quota
    )
    schema = NetworkServiceReadExtendedPublic.from_orm(
        db_network_serv_with_single_quota
    )
    validate_read_extended_public_network_service_attrs(
        obj_out=schema, db_item=db_network_serv_with_single_quota
    )


def test_read_schema_with_multiple_quotas(
    db_network_serv_with_multiple_quotas: NetworkService,
):
    """Create a valid 'Read' Schema from DB object.

    Apply conversion for this item for all read schemas. No one of them should raise
    errors.

    Target service is linked to multiple block storage quotas.
    """
    schema = NetworkServiceRead.from_orm(db_network_serv_with_multiple_quotas)
    validate_read_network_service_attrs(
        obj_out=schema, db_item=db_network_serv_with_multiple_quotas
    )
    schema = NetworkServiceReadShort.from_orm(db_network_serv_with_multiple_quotas)
    validate_read_short_network_service_attrs(
        obj_out=schema, db_item=db_network_serv_with_multiple_quotas
    )
    schema = NetworkServiceReadPublic.from_orm(db_network_serv_with_multiple_quotas)
    validate_read_public_network_service_attrs(
        obj_out=schema, db_item=db_network_serv_with_multiple_quotas
    )
    schema = NetworkServiceReadExtended.from_orm(db_network_serv_with_multiple_quotas)
    assert len(schema.quotas) > 1
    validate_read_extended_network_service_attrs(
        obj_out=schema, db_item=db_network_serv_with_multiple_quotas
    )
    schema = NetworkServiceReadExtendedPublic.from_orm(
        db_network_serv_with_multiple_quotas
    )
    assert len(schema.quotas) > 1
    validate_read_extended_public_network_service_attrs(
        obj_out=schema, db_item=db_network_serv_with_multiple_quotas
    )
