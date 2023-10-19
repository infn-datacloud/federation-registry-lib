import pytest
from app.region.models import Region
from app.service.crud import identity_service
from app.service.enum import (
    BlockStorageServiceName,
    ComputeServiceName,
    NetworkServiceName,
    ServiceType,
)
from app.service.schemas import (
    IdentityServiceRead,
    IdentityServiceReadPublic,
    IdentityServiceReadShort,
)
from app.service.schemas_extended import (
    IdentityServiceReadExtended,
    IdentityServiceReadExtendedPublic,
)
from app.tests.utils.service import create_random_identity_service
from app.tests.utils.utils import random_lower_string
from pydantic import ValidationError


def test_create_schema():
    """Create a valid 'Create' Schema."""
    create_random_identity_service()
    create_random_identity_service(default=True)


def test_invalid_create_schema():
    """List all invalid situations for a 'Create' Schema."""
    a = create_random_identity_service()
    with pytest.raises(ValidationError):
        a.type = ServiceType.BLOCK_STORAGE.value
    with pytest.raises(ValidationError):
        a.type = ServiceType.COMPUTE.value
    with pytest.raises(ValidationError):
        a.type = ServiceType.NETWORK.value
    with pytest.raises(ValidationError):
        a.type = random_lower_string()
    with pytest.raises(ValidationError):
        a.name = BlockStorageServiceName.OPENSTACK_CINDER.value
    with pytest.raises(ValidationError):
        a.name = ComputeServiceName.OPENSTACK_NOVA.value
    with pytest.raises(ValidationError):
        a.name = NetworkServiceName.OPENSTACK_NEUTRON.value
    with pytest.raises(ValidationError):
        a.name = random_lower_string()
    with pytest.raises(ValidationError):
        a.endpoint = None


def test_read_schema(db_region: Region):
    """Create a valid 'Read' Schema."""
    obj_in = create_random_identity_service()
    db_obj = identity_service.create(obj_in=obj_in, region=db_region)
    IdentityServiceRead.from_orm(db_obj)
    IdentityServiceReadPublic.from_orm(db_obj)
    IdentityServiceReadShort.from_orm(db_obj)
    IdentityServiceReadExtended.from_orm(db_obj)
    IdentityServiceReadExtendedPublic.from_orm(db_obj)

    obj_in = create_random_identity_service(default=True)
    db_obj = identity_service.update(db_obj=db_obj, obj_in=obj_in, force=True)
    IdentityServiceRead.from_orm(db_obj)
    IdentityServiceReadPublic.from_orm(db_obj)
    IdentityServiceReadShort.from_orm(db_obj)
    IdentityServiceReadExtended.from_orm(db_obj)
    IdentityServiceReadExtendedPublic.from_orm(db_obj)
