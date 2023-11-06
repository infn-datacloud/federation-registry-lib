import pytest
from app.service.enum import (
    BlockStorageServiceName,
    ComputeServiceName,
    NetworkServiceName,
    ServiceType,
)
from app.service.models import IdentityService
from app.service.schemas import (
    IdentityServiceRead,
    IdentityServiceReadPublic,
    IdentityServiceReadShort,
)
from app.service.schemas_extended import (
    IdentityServiceReadExtended,
    IdentityServiceReadExtendedPublic,
)
from pydantic import ValidationError
from tests.utils.identity_service import (
    create_random_identity_service,
    validate_read_extended_identity_service_attrs,
    validate_read_extended_public_identity_service_attrs,
    validate_read_identity_service_attrs,
    validate_read_public_identity_service_attrs,
    validate_read_short_identity_service_attrs,
)
from tests.utils.utils import random_lower_string


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


def test_read_schema(db_identity_serv: IdentityService):
    """Create a valid 'Read' Schema from DB object.

    Apply conversion for this item for all read schemas. No one of them should raise
    errors.

    Target service is linked only to the parent region.
    """
    schema = IdentityServiceRead.from_orm(db_identity_serv)
    validate_read_identity_service_attrs(obj_out=schema, db_item=db_identity_serv)
    schema = IdentityServiceReadShort.from_orm(db_identity_serv)
    validate_read_short_identity_service_attrs(obj_out=schema, db_item=db_identity_serv)
    schema = IdentityServiceReadPublic.from_orm(db_identity_serv)
    validate_read_public_identity_service_attrs(
        obj_out=schema, db_item=db_identity_serv
    )
    schema = IdentityServiceReadExtended.from_orm(db_identity_serv)
    validate_read_extended_identity_service_attrs(
        obj_out=schema, db_item=db_identity_serv
    )
    schema = IdentityServiceReadExtendedPublic.from_orm(db_identity_serv)
    validate_read_extended_public_identity_service_attrs(
        obj_out=schema, db_item=db_identity_serv
    )
