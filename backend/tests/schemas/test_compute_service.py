import copy
from uuid import uuid4

import pytest
from app.service.enum import (
    BlockStorageServiceName,
    IdentityServiceName,
    NetworkServiceName,
    ServiceType,
)
from app.service.models import ComputeService
from app.service.schemas import (
    ComputeServiceRead,
    ComputeServiceReadPublic,
    ComputeServiceReadShort,
)
from app.service.schemas_extended import (
    ComputeServiceReadExtended,
    ComputeServiceReadExtendedPublic,
)
from pydantic import ValidationError
from tests.utils.compute_service import (
    create_random_compute_service,
    validate_read_compute_service_attrs,
    validate_read_extended_compute_service_attrs,
    validate_read_extended_public_compute_service_attrs,
    validate_read_public_compute_service_attrs,
    validate_read_short_compute_service_attrs,
)
from tests.utils.utils import random_lower_string


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


def test_read_schema(db_compute_serv: ComputeService):
    """Create a valid 'Read' Schema from DB object.

    Apply conversion for this item for all read schemas. No one of them
    should raise errors.

    Target service is linked only to the parent region.
    """
    schema = ComputeServiceRead.from_orm(db_compute_serv)
    validate_read_compute_service_attrs(obj_out=schema, db_item=db_compute_serv)
    schema = ComputeServiceReadShort.from_orm(db_compute_serv)
    validate_read_short_compute_service_attrs(obj_out=schema, db_item=db_compute_serv)
    schema = ComputeServiceReadPublic.from_orm(db_compute_serv)
    validate_read_public_compute_service_attrs(obj_out=schema, db_item=db_compute_serv)
    schema = ComputeServiceReadExtended.from_orm(db_compute_serv)
    validate_read_extended_compute_service_attrs(
        obj_out=schema, db_item=db_compute_serv
    )
    schema = ComputeServiceReadExtendedPublic.from_orm(db_compute_serv)
    validate_read_extended_public_compute_service_attrs(
        obj_out=schema, db_item=db_compute_serv
    )


def test_read_schema_with_single_quota(
    db_compute_serv_with_single_quota: ComputeService,
):
    """Create a valid 'Read' Schema from DB object.

    Apply conversion for this item for all read schemas. No one of them
    should raise errors.

    Target service is linked only to one compute quota.
    """
    schema = ComputeServiceRead.from_orm(db_compute_serv_with_single_quota)
    validate_read_compute_service_attrs(
        obj_out=schema, db_item=db_compute_serv_with_single_quota
    )
    schema = ComputeServiceReadShort.from_orm(db_compute_serv_with_single_quota)
    validate_read_short_compute_service_attrs(
        obj_out=schema, db_item=db_compute_serv_with_single_quota
    )
    schema = ComputeServiceReadPublic.from_orm(db_compute_serv_with_single_quota)
    validate_read_public_compute_service_attrs(
        obj_out=schema, db_item=db_compute_serv_with_single_quota
    )
    schema = ComputeServiceReadExtended.from_orm(db_compute_serv_with_single_quota)
    validate_read_extended_compute_service_attrs(
        obj_out=schema, db_item=db_compute_serv_with_single_quota
    )
    schema = ComputeServiceReadExtendedPublic.from_orm(
        db_compute_serv_with_single_quota
    )
    validate_read_extended_public_compute_service_attrs(
        obj_out=schema, db_item=db_compute_serv_with_single_quota
    )


def test_read_schema_with_multiple_quotas(
    db_compute_serv_with_multiple_quotas: ComputeService,
):
    """Create a valid 'Read' Schema from DB object.

    Apply conversion for this item for all read schemas. No one of them
    should raise errors.

    Target service is linked multiple compute quotas.
    """
    schema = ComputeServiceRead.from_orm(db_compute_serv_with_multiple_quotas)
    validate_read_compute_service_attrs(
        obj_out=schema, db_item=db_compute_serv_with_multiple_quotas
    )
    schema = ComputeServiceReadShort.from_orm(db_compute_serv_with_multiple_quotas)
    validate_read_short_compute_service_attrs(
        obj_out=schema, db_item=db_compute_serv_with_multiple_quotas
    )
    schema = ComputeServiceReadPublic.from_orm(db_compute_serv_with_multiple_quotas)
    validate_read_public_compute_service_attrs(
        obj_out=schema, db_item=db_compute_serv_with_multiple_quotas
    )
    schema = ComputeServiceReadExtended.from_orm(db_compute_serv_with_multiple_quotas)
    assert len(schema.quotas) > 1
    validate_read_extended_compute_service_attrs(
        obj_out=schema, db_item=db_compute_serv_with_multiple_quotas
    )
    schema = ComputeServiceReadExtendedPublic.from_orm(
        db_compute_serv_with_multiple_quotas
    )
    assert len(schema.quotas) > 1
    validate_read_extended_public_compute_service_attrs(
        obj_out=schema, db_item=db_compute_serv_with_multiple_quotas
    )


def test_read_schema_with_single_flavor(
    db_compute_serv_with_single_flavor: ComputeService,
):
    """Create a valid 'Read' Schema from DB object.

    Apply conversion for this item for all read schemas. No one of them
    should raise errors.

    Target service is linked only to one flavor.
    """
    schema = ComputeServiceRead.from_orm(db_compute_serv_with_single_flavor)
    validate_read_compute_service_attrs(
        obj_out=schema, db_item=db_compute_serv_with_single_flavor
    )
    schema = ComputeServiceReadShort.from_orm(db_compute_serv_with_single_flavor)
    validate_read_short_compute_service_attrs(
        obj_out=schema, db_item=db_compute_serv_with_single_flavor
    )
    schema = ComputeServiceReadPublic.from_orm(db_compute_serv_with_single_flavor)
    validate_read_public_compute_service_attrs(
        obj_out=schema, db_item=db_compute_serv_with_single_flavor
    )
    schema = ComputeServiceReadExtended.from_orm(db_compute_serv_with_single_flavor)
    validate_read_extended_compute_service_attrs(
        obj_out=schema, db_item=db_compute_serv_with_single_flavor
    )
    schema = ComputeServiceReadExtendedPublic.from_orm(
        db_compute_serv_with_single_flavor
    )
    validate_read_extended_public_compute_service_attrs(
        obj_out=schema, db_item=db_compute_serv_with_single_flavor
    )


def test_read_schema_with_multiple_flavors(
    db_compute_serv_with_multiple_flavors: ComputeService,
):
    """Create a valid 'Read' Schema from DB object.

    Apply conversion for this item for all read schemas. No one of them
    should raise errors.

    Target service is linked multiple flavors.
    """
    schema = ComputeServiceRead.from_orm(db_compute_serv_with_multiple_flavors)
    validate_read_compute_service_attrs(
        obj_out=schema, db_item=db_compute_serv_with_multiple_flavors
    )
    schema = ComputeServiceReadShort.from_orm(db_compute_serv_with_multiple_flavors)
    validate_read_short_compute_service_attrs(
        obj_out=schema, db_item=db_compute_serv_with_multiple_flavors
    )
    schema = ComputeServiceReadPublic.from_orm(db_compute_serv_with_multiple_flavors)
    validate_read_public_compute_service_attrs(
        obj_out=schema, db_item=db_compute_serv_with_multiple_flavors
    )
    schema = ComputeServiceReadExtended.from_orm(db_compute_serv_with_multiple_flavors)
    assert len(schema.flavors) > 1
    validate_read_extended_compute_service_attrs(
        obj_out=schema, db_item=db_compute_serv_with_multiple_flavors
    )
    schema = ComputeServiceReadExtendedPublic.from_orm(
        db_compute_serv_with_multiple_flavors
    )
    assert len(schema.flavors) > 1
    validate_read_extended_public_compute_service_attrs(
        obj_out=schema, db_item=db_compute_serv_with_multiple_flavors
    )


def test_read_schema_with_single_image(
    db_compute_serv_with_single_image: ComputeService,
):
    """Create a valid 'Read' Schema from DB object.

    Apply conversion for this item for all read schemas. No one of them
    should raise errors.

    Target service is linked only to one image.
    """
    schema = ComputeServiceRead.from_orm(db_compute_serv_with_single_image)
    validate_read_compute_service_attrs(
        obj_out=schema, db_item=db_compute_serv_with_single_image
    )
    schema = ComputeServiceReadShort.from_orm(db_compute_serv_with_single_image)
    validate_read_short_compute_service_attrs(
        obj_out=schema, db_item=db_compute_serv_with_single_image
    )
    schema = ComputeServiceReadPublic.from_orm(db_compute_serv_with_single_image)
    validate_read_public_compute_service_attrs(
        obj_out=schema, db_item=db_compute_serv_with_single_image
    )
    schema = ComputeServiceReadExtended.from_orm(db_compute_serv_with_single_image)
    validate_read_extended_compute_service_attrs(
        obj_out=schema, db_item=db_compute_serv_with_single_image
    )
    schema = ComputeServiceReadExtendedPublic.from_orm(
        db_compute_serv_with_single_image
    )
    validate_read_extended_public_compute_service_attrs(
        obj_out=schema, db_item=db_compute_serv_with_single_image
    )


def test_read_schema_with_multiple_images(
    db_compute_serv_with_multiple_images: ComputeService,
):
    """Create a valid 'Read' Schema from DB object.

    Apply conversion for this item for all read schemas. No one of them
    should raise errors.

    Target service is linked multiple images.
    """
    schema = ComputeServiceRead.from_orm(db_compute_serv_with_multiple_images)
    validate_read_compute_service_attrs(
        obj_out=schema, db_item=db_compute_serv_with_multiple_images
    )
    schema = ComputeServiceReadShort.from_orm(db_compute_serv_with_multiple_images)
    validate_read_short_compute_service_attrs(
        obj_out=schema, db_item=db_compute_serv_with_multiple_images
    )
    schema = ComputeServiceReadPublic.from_orm(db_compute_serv_with_multiple_images)
    validate_read_public_compute_service_attrs(
        obj_out=schema, db_item=db_compute_serv_with_multiple_images
    )
    schema = ComputeServiceReadExtended.from_orm(db_compute_serv_with_multiple_images)
    assert len(schema.images) > 1
    validate_read_extended_compute_service_attrs(
        obj_out=schema, db_item=db_compute_serv_with_multiple_images
    )
    schema = ComputeServiceReadExtendedPublic.from_orm(
        db_compute_serv_with_multiple_images
    )
    assert len(schema.images) > 1
    validate_read_extended_public_compute_service_attrs(
        obj_out=schema, db_item=db_compute_serv_with_multiple_images
    )
