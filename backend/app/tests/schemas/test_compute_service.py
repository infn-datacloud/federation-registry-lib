import copy
from uuid import uuid4

import pytest
from app.region.models import Region
from app.service.crud import compute_service
from app.service.enum import (
    BlockStorageServiceName,
    IdentityServiceName,
    NetworkServiceName,
    ServiceType,
)
from app.service.schemas import (
    ComputeServiceRead,
    ComputeServiceReadPublic,
    ComputeServiceReadShort,
)
from app.service.schemas_extended import (
    ComputeServiceReadExtended,
    ComputeServiceReadExtendedPublic,
)
from app.tests.utils.compute_service import create_random_compute_service
from app.tests.utils.utils import random_lower_string
from pydantic import ValidationError


def test_create_schema():
    create_random_compute_service()
    create_random_compute_service(default=True)
    create_random_compute_service(projects=[uuid4()])
    create_random_compute_service(default=True, projects=[uuid4()])
    create_random_compute_service(with_flavors=True)
    create_random_compute_service(default=True, with_flavors=True)
    create_random_compute_service(with_flavors=True)
    create_random_compute_service(default=True, with_flavors=True, projects=[uuid4()])
    create_random_compute_service(with_images=True)
    create_random_compute_service(default=True, with_images=True)
    create_random_compute_service(default=True, with_images=True, projects=[uuid4()])
    create_random_compute_service(with_flavors=True, with_images=True)
    create_random_compute_service(default=True, with_flavors=True, with_images=True)
    create_random_compute_service(
        with_flavors=True, with_images=True, projects=[uuid4()]
    )
    item = create_random_compute_service(
        default=True, with_flavors=True, with_images=True, projects=[uuid4()]
    )
    # 2 Quotas related to the same project. One total and one per user.
    q1 = item.quotas[0]
    q2 = copy.deepcopy(q1)
    q2.per_user = not q1.per_user
    item.quotas = [q1, q2]


def test_invalid_create_schema():
    a = create_random_compute_service(
        with_flavors=True, with_images=True, projects=[uuid4()]
    )
    with pytest.raises(ValidationError):
        a.type = ServiceType.BLOCK_STORAGE.value
    with pytest.raises(ValidationError):
        a.type = ServiceType.IDENTITY.value
    with pytest.raises(ValidationError):
        a.type = ServiceType.NETWORK.value
    with pytest.raises(ValidationError):
        a.type = random_lower_string()
    with pytest.raises(ValidationError):
        a.name = BlockStorageServiceName.OPENSTACK_CINDER.value
    with pytest.raises(ValidationError):
        a.name = IdentityServiceName.OPENSTACK_KEYSTONE.value
    with pytest.raises(ValidationError):
        a.name = NetworkServiceName.OPENSTACK_NEUTRON.value
    with pytest.raises(ValidationError):
        a.type = random_lower_string()
    with pytest.raises(ValidationError):
        a.endpoint = None
    with pytest.raises(ValidationError):
        # Duplicated flavors
        a.flavors = [a.flavors[0], a.flavors[0]]
    with pytest.raises(ValidationError):
        # Duplicated images
        a.images = [a.images[0], a.images[0]]
    with pytest.raises(ValidationError):
        # Duplicated quotas
        a.quotas = [a.quotas[0], a.quotas[0]]


def test_read_schema(db_region: Region):
    """Create a valid 'Read' Schema."""
    obj_in = create_random_compute_service()
    db_obj = compute_service.create(obj_in=obj_in, region=db_region)
    ComputeServiceRead.from_orm(db_obj)
    ComputeServiceReadPublic.from_orm(db_obj)
    ComputeServiceReadShort.from_orm(db_obj)
    ComputeServiceReadExtended.from_orm(db_obj)
    ComputeServiceReadExtendedPublic.from_orm(db_obj)

    obj_in = create_random_compute_service(default=True)
    db_obj = compute_service.update(db_obj=db_obj, obj_in=obj_in, force=True)
    ComputeServiceRead.from_orm(db_obj)
    ComputeServiceReadPublic.from_orm(db_obj)
    ComputeServiceReadShort.from_orm(db_obj)
    ComputeServiceReadExtended.from_orm(db_obj)
    ComputeServiceReadExtendedPublic.from_orm(db_obj)

    obj_in = create_random_compute_service(with_flavors=True)
    db_obj = compute_service.update(db_obj=db_obj, obj_in=obj_in, force=True)
    ComputeServiceRead.from_orm(db_obj)
    ComputeServiceReadPublic.from_orm(db_obj)
    ComputeServiceReadShort.from_orm(db_obj)
    ComputeServiceReadExtended.from_orm(db_obj)
    ComputeServiceReadExtendedPublic.from_orm(db_obj)

    obj_in = create_random_compute_service(default=True, with_flavors=True)
    db_obj = compute_service.update(db_obj=db_obj, obj_in=obj_in, force=True)
    ComputeServiceRead.from_orm(db_obj)
    ComputeServiceReadPublic.from_orm(db_obj)
    ComputeServiceReadShort.from_orm(db_obj)
    ComputeServiceReadExtended.from_orm(db_obj)
    ComputeServiceReadExtendedPublic.from_orm(db_obj)

    obj_in = create_random_compute_service(with_images=True)
    db_obj = compute_service.update(db_obj=db_obj, obj_in=obj_in, force=True)
    ComputeServiceRead.from_orm(db_obj)
    ComputeServiceReadPublic.from_orm(db_obj)
    ComputeServiceReadShort.from_orm(db_obj)
    ComputeServiceReadExtended.from_orm(db_obj)
    ComputeServiceReadExtendedPublic.from_orm(db_obj)

    obj_in = create_random_compute_service(default=True, with_images=True)
    db_obj = compute_service.update(db_obj=db_obj, obj_in=obj_in, force=True)
    ComputeServiceRead.from_orm(db_obj)
    ComputeServiceReadPublic.from_orm(db_obj)
    ComputeServiceReadShort.from_orm(db_obj)
    ComputeServiceReadExtended.from_orm(db_obj)
    ComputeServiceReadExtendedPublic.from_orm(db_obj)

    db_provider = db_region.provider.single()
    obj_in = create_random_compute_service(
        projects=[i.uuid for i in db_provider.projects]
    )
    db_obj = compute_service.update(
        db_obj=db_obj, obj_in=obj_in, projects=db_provider.projects, force=True
    )
    ComputeServiceRead.from_orm(db_obj)
    ComputeServiceReadPublic.from_orm(db_obj)
    ComputeServiceReadShort.from_orm(db_obj)
    ComputeServiceReadExtended.from_orm(db_obj)
    ComputeServiceReadExtendedPublic.from_orm(db_obj)

    obj_in = create_random_compute_service(
        default=True, projects=[i.uuid for i in db_provider.projects]
    )
    db_obj = compute_service.update(
        db_obj=db_obj, obj_in=obj_in, projects=db_provider.projects, force=True
    )
    ComputeServiceRead.from_orm(db_obj)
    ComputeServiceReadPublic.from_orm(db_obj)
    ComputeServiceReadShort.from_orm(db_obj)
    ComputeServiceReadExtended.from_orm(db_obj)
    ComputeServiceReadExtendedPublic.from_orm(db_obj)

    obj_in = create_random_compute_service(
        with_flavors=True, projects=[i.uuid for i in db_provider.projects]
    )
    db_obj = compute_service.update(
        db_obj=db_obj, obj_in=obj_in, projects=db_provider.projects, force=True
    )
    ComputeServiceRead.from_orm(db_obj)
    ComputeServiceReadPublic.from_orm(db_obj)
    ComputeServiceReadShort.from_orm(db_obj)
    ComputeServiceReadExtended.from_orm(db_obj)
    ComputeServiceReadExtendedPublic.from_orm(db_obj)

    obj_in = create_random_compute_service(
        default=True, with_flavors=True, projects=[i.uuid for i in db_provider.projects]
    )
    db_obj = compute_service.update(
        db_obj=db_obj, obj_in=obj_in, projects=db_provider.projects, force=True
    )
    ComputeServiceRead.from_orm(db_obj)
    ComputeServiceReadPublic.from_orm(db_obj)
    ComputeServiceReadShort.from_orm(db_obj)
    ComputeServiceReadExtended.from_orm(db_obj)
    ComputeServiceReadExtendedPublic.from_orm(db_obj)

    obj_in = create_random_compute_service(
        with_images=True, projects=[i.uuid for i in db_provider.projects]
    )
    db_obj = compute_service.update(
        db_obj=db_obj, obj_in=obj_in, projects=db_provider.projects, force=True
    )
    ComputeServiceRead.from_orm(db_obj)
    ComputeServiceReadPublic.from_orm(db_obj)
    ComputeServiceReadShort.from_orm(db_obj)
    ComputeServiceReadExtended.from_orm(db_obj)
    ComputeServiceReadExtendedPublic.from_orm(db_obj)

    obj_in = create_random_compute_service(
        default=True, with_images=True, projects=[i.uuid for i in db_provider.projects]
    )
    db_obj = compute_service.update(
        db_obj=db_obj, obj_in=obj_in, projects=db_provider.projects, force=True
    )
    ComputeServiceRead.from_orm(db_obj)
    ComputeServiceReadPublic.from_orm(db_obj)
    ComputeServiceReadShort.from_orm(db_obj)
    ComputeServiceReadExtended.from_orm(db_obj)
    ComputeServiceReadExtendedPublic.from_orm(db_obj)

    obj_in = create_random_compute_service(
        with_images=True,
        with_flavors=True,
        projects=[i.uuid for i in db_provider.projects],
    )
    db_obj = compute_service.update(
        db_obj=db_obj, obj_in=obj_in, projects=db_provider.projects, force=True
    )
    ComputeServiceRead.from_orm(db_obj)
    ComputeServiceReadPublic.from_orm(db_obj)
    ComputeServiceReadShort.from_orm(db_obj)
    ComputeServiceReadExtended.from_orm(db_obj)
    ComputeServiceReadExtendedPublic.from_orm(db_obj)

    obj_in = create_random_compute_service(
        default=True,
        with_images=True,
        with_flavors=True,
        projects=[i.uuid for i in db_provider.projects],
    )
    db_obj = compute_service.update(
        db_obj=db_obj, obj_in=obj_in, projects=db_provider.projects, force=True
    )
    ComputeServiceRead.from_orm(db_obj)
    ComputeServiceReadPublic.from_orm(db_obj)
    ComputeServiceReadShort.from_orm(db_obj)
    ComputeServiceReadExtended.from_orm(db_obj)
    ComputeServiceReadExtendedPublic.from_orm(db_obj)
