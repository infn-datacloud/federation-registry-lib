import copy
from uuid import uuid4

import pytest
from app.region.models import Region
from app.service.crud import block_storage_service
from app.service.enum import (
    ComputeServiceName,
    IdentityServiceName,
    NetworkServiceName,
    ServiceType,
)
from app.service.schemas import (
    BlockStorageServiceRead,
    BlockStorageServiceReadPublic,
    BlockStorageServiceReadShort,
)
from app.service.schemas_extended import (
    BlockStorageServiceReadExtended,
    BlockStorageServiceReadExtendedPublic,
)
from app.tests.utils.block_storage_service import create_random_block_storage_service
from app.tests.utils.utils import random_lower_string
from pydantic import ValidationError


def test_create_schema():
    """Create a valid 'Create' Schema."""
    create_random_block_storage_service()
    create_random_block_storage_service(default=True)
    create_random_block_storage_service(projects=[uuid4()])
    item = create_random_block_storage_service(default=True, projects=[uuid4()])
    # 2 Quotas related to the same project. One total and one per user.
    q1 = item.quotas[0]
    q2 = copy.deepcopy(q1)
    q2.per_user = not q1.per_user
    item.quotas = [q1, q2]


def test_invalid_create_schema():
    """List all invalid situations for a 'Create' Schema."""
    a = create_random_block_storage_service(projects=[uuid4()])
    with pytest.raises(ValidationError):
        a.type = ServiceType.COMPUTE.value
    with pytest.raises(ValidationError):
        a.type = ServiceType.IDENTITY.value
    with pytest.raises(ValidationError):
        a.type = ServiceType.NETWORK.value
    with pytest.raises(ValidationError):
        a.type = random_lower_string()
    with pytest.raises(ValidationError):
        a.name = ComputeServiceName.OPENSTACK_NOVA.value
    with pytest.raises(ValidationError):
        a.name = IdentityServiceName.OPENSTACK_KEYSTONE.value
    with pytest.raises(ValidationError):
        a.name = NetworkServiceName.OPENSTACK_NEUTRON.value
    with pytest.raises(ValidationError):
        a.type = random_lower_string()
    with pytest.raises(ValidationError):
        a.endpoint = None
    with pytest.raises(ValidationError):
        # Duplicated quotas
        a.quotas = [a.quotas[0], a.quotas[0]]


def test_read_schema(db_region: Region):
    """Create a valid 'Read' Schema."""
    obj_in = create_random_block_storage_service()
    db_obj = block_storage_service.create(obj_in=obj_in, region=db_region)
    BlockStorageServiceRead.from_orm(db_obj)
    BlockStorageServiceReadPublic.from_orm(db_obj)
    BlockStorageServiceReadShort.from_orm(db_obj)
    BlockStorageServiceReadExtended.from_orm(db_obj)
    BlockStorageServiceReadExtendedPublic.from_orm(db_obj)

    obj_in = create_random_block_storage_service(default=True)
    db_obj = block_storage_service.update(db_obj=db_obj, obj_in=obj_in, force=True)
    BlockStorageServiceRead.from_orm(db_obj)
    BlockStorageServiceReadPublic.from_orm(db_obj)
    BlockStorageServiceReadShort.from_orm(db_obj)
    BlockStorageServiceReadExtended.from_orm(db_obj)
    BlockStorageServiceReadExtendedPublic.from_orm(db_obj)

    db_provider = db_region.provider.single()
    obj_in = create_random_block_storage_service(
        projects=[i.uuid for i in db_provider.projects]
    )
    db_obj = block_storage_service.update(
        db_obj=db_obj, obj_in=obj_in, projects=db_provider.projects, force=True
    )
    BlockStorageServiceRead.from_orm(db_obj)
    BlockStorageServiceReadPublic.from_orm(db_obj)
    BlockStorageServiceReadShort.from_orm(db_obj)
    BlockStorageServiceReadExtended.from_orm(db_obj)
    BlockStorageServiceReadExtendedPublic.from_orm(db_obj)

    obj_in = create_random_block_storage_service(
        default=True, projects=[i.uuid for i in db_provider.projects]
    )
    db_obj = block_storage_service.update(
        db_obj=db_obj, obj_in=obj_in, projects=db_provider.projects, force=True
    )
    BlockStorageServiceRead.from_orm(db_obj)
    BlockStorageServiceReadPublic.from_orm(db_obj)
    BlockStorageServiceReadShort.from_orm(db_obj)
    BlockStorageServiceReadExtended.from_orm(db_obj)
    BlockStorageServiceReadExtendedPublic.from_orm(db_obj)
