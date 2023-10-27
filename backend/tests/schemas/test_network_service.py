from uuid import uuid4

import pytest
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
from pydantic import ValidationError
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


def test_read_schema(db_network_serv: NetworkService):
    """Create a valid 'Read' Schema from DB object.

    Apply conversion for this item for all read schemas. No one of them
    should raise errors.

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


# def test_read_schema(db_region: Region):
#     """Create a valid 'Read' Schema."""
#     obj_in = create_random_network_service()
#     db_obj = network_service.create(obj_in=obj_in, region=db_region)
#     NetworkServiceRead.from_orm(db_obj)
#     NetworkServiceReadPublic.from_orm(db_obj)
#     NetworkServiceReadShort.from_orm(db_obj)
#     NetworkServiceReadExtended.from_orm(db_obj)
#     NetworkServiceReadExtendedPublic.from_orm(db_obj)

#     obj_in = create_random_network_service(default=True)
#     db_obj = network_service.update(db_obj=db_obj, obj_in=obj_in, force=True)
#     NetworkServiceRead.from_orm(db_obj)
#     NetworkServiceReadPublic.from_orm(db_obj)
#     NetworkServiceReadShort.from_orm(db_obj)
#     NetworkServiceReadExtended.from_orm(db_obj)
#     NetworkServiceReadExtendedPublic.from_orm(db_obj)

#     obj_in = create_random_network_service(with_networks=True)
#     db_obj = network_service.update(db_obj=db_obj, obj_in=obj_in, force=True)
#     NetworkServiceRead.from_orm(db_obj)
#     NetworkServiceReadPublic.from_orm(db_obj)
#     NetworkServiceReadShort.from_orm(db_obj)
#     NetworkServiceReadExtended.from_orm(db_obj)
#     NetworkServiceReadExtendedPublic.from_orm(db_obj)

#     obj_in = create_random_network_service(default=True, with_networks=True)
#     db_obj = network_service.update(db_obj=db_obj, obj_in=obj_in, force=True)
#     NetworkServiceRead.from_orm(db_obj)
#     NetworkServiceReadPublic.from_orm(db_obj)
#     NetworkServiceReadShort.from_orm(db_obj)
#     NetworkServiceReadExtended.from_orm(db_obj)
#     NetworkServiceReadExtendedPublic.from_orm(db_obj)

#     db_provider = db_region.provider.single()
#     obj_in = create_random_network_service(
#         with_networks=True, projects=[i.uuid for i in db_provider.projects]
#     )
#     db_obj = network_service.update(
#         db_obj=db_obj, obj_in=obj_in, projects=db_provider.projects, force=True
#     )
#     NetworkServiceRead.from_orm(db_obj)
#     NetworkServiceReadPublic.from_orm(db_obj)
#     NetworkServiceReadShort.from_orm(db_obj)
#     NetworkServiceReadExtended.from_orm(db_obj)
#     NetworkServiceReadExtendedPublic.from_orm(db_obj)

#     obj_in = create_random_network_service(
#         default=True,
#         with_networks=True,
#         projects=[i.uuid for i in db_provider.projects],
#     )
#     db_obj = network_service.update(
#         db_obj=db_obj, obj_in=obj_in, projects=db_provider.projects, force=True
#     )
#     NetworkServiceRead.from_orm(db_obj)
#     NetworkServiceReadPublic.from_orm(db_obj)
#     NetworkServiceReadShort.from_orm(db_obj)
#     NetworkServiceReadExtended.from_orm(db_obj)
#     NetworkServiceReadExtendedPublic.from_orm(db_obj)
