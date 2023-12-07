from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.region.models import Region
from app.region.schemas import RegionRead, RegionReadPublic
from app.region.schemas_extended import (
    RegionReadExtended,
    RegionReadExtendedPublic,
)
from tests.utils.region import (
    create_random_region,
    validate_read_extended_public_region_attrs,
    validate_read_extended_region_attrs,
    validate_read_public_region_attrs,
    validate_read_region_attrs,
)


def test_create_schema():
    create_random_region()
    create_random_region(default=True)
    create_random_region(with_location=True)
    create_random_region(default=True, with_location=True)
    create_random_region(with_block_storage_services=True)
    create_random_region(default=True, with_block_storage_services=True)
    create_random_region(with_block_storage_services=True, projects=[uuid4()])
    create_random_region(
        default=True, with_block_storage_services=True, projects=[uuid4()]
    )
    create_random_region(with_compute_services=True)
    create_random_region(default=True, with_compute_services=True)
    create_random_region(with_compute_services=True, projects=[uuid4()])
    create_random_region(default=True, with_compute_services=True, projects=[uuid4()])
    create_random_region(with_identity_services=True)
    create_random_region(default=True, with_identity_services=True)
    create_random_region(with_network_services=True)
    create_random_region(default=True, with_network_services=True)
    create_random_region(with_network_services=True, projects=[uuid4()])
    create_random_region(default=True, with_network_services=True, projects=[uuid4()])
    create_random_region(
        with_location=True,
        with_block_storage_services=True,
        with_compute_services=True,
        with_identity_services=True,
        with_network_services=True,
    )
    create_random_region(
        default=True,
        with_location=True,
        with_block_storage_services=True,
        with_compute_services=True,
        with_identity_services=True,
        with_network_services=True,
    )
    create_random_region(
        with_location=True,
        with_block_storage_services=True,
        with_compute_services=True,
        with_identity_services=True,
        with_network_services=True,
    )
    create_random_region(
        with_location=True,
        with_block_storage_services=True,
        with_compute_services=True,
        with_identity_services=True,
        with_network_services=True,
        projects=[uuid4()],
    )
    create_random_region(
        default=True,
        with_location=True,
        with_block_storage_services=True,
        with_compute_services=True,
        with_identity_services=True,
        with_network_services=True,
        projects=[uuid4()],
    )


def test_invalid_create_schema():
    a = create_random_region(
        with_location=True,
        with_block_storage_services=True,
        with_compute_services=True,
        with_identity_services=True,
        with_network_services=True,
        projects=[uuid4()],
    )
    with pytest.raises(ValidationError):
        a.name = None
    with pytest.raises(ValidationError):
        # Duplicated block storage services
        a.block_storage_services = [
            a.block_storage_services[0],
            a.block_storage_services[0],
        ]
    with pytest.raises(ValidationError):
        # Duplicated compute services
        a.compute_services = [a.compute_services[0], a.compute_services[0]]
    with pytest.raises(ValidationError):
        # Duplicated identity services
        a.identity_services = [a.identity_services[0], a.identity_services[0]]
    with pytest.raises(ValidationError):
        # Duplicated network services
        a.network_services = [a.network_services[0], a.network_services[0]]


def test_read_schema(db_region: Region):
    """Create a valid 'Read' from DB object.

    Apply conversion for this item for all read schemas. No one of them should raise
    errors.

    Target region is only linked to the provider.
    """
    schema = RegionRead.from_orm(db_region)
    validate_read_region_attrs(obj_out=schema, db_item=db_region)
    schema = RegionReadPublic.from_orm(db_region)
    validate_read_public_region_attrs(obj_out=schema, db_item=db_region)
    schema = RegionReadExtended.from_orm(db_region)
    validate_read_extended_region_attrs(obj_out=schema, db_item=db_region)
    schema = RegionReadExtendedPublic.from_orm(db_region)
    validate_read_extended_public_region_attrs(obj_out=schema, db_item=db_region)


def test_read_schema_with_location(db_region_with_location: Region):
    """Create a valid 'Read' from DB object.

    Apply conversion for this item for all read schemas. No one of them should raise
    errors.

    Target region has a location.
    """
    schema = RegionRead.from_orm(db_region_with_location)
    validate_read_region_attrs(obj_out=schema, db_item=db_region_with_location)
    schema = RegionReadPublic.from_orm(db_region_with_location)
    validate_read_public_region_attrs(obj_out=schema, db_item=db_region_with_location)
    schema = RegionReadExtended.from_orm(db_region_with_location)
    validate_read_extended_region_attrs(obj_out=schema, db_item=db_region_with_location)
    schema = RegionReadExtendedPublic.from_orm(db_region_with_location)
    validate_read_extended_public_region_attrs(
        obj_out=schema, db_item=db_region_with_location
    )


def test_read_schema_with_single_block_storage_service(
    db_region_with_block_storage_service: Region,
):
    """Create a valid 'Read' from DB object.

    Apply conversion for this item for all read schemas. No one of them should raise
    errors.

    Target region has a block storage service.
    """
    schema = RegionRead.from_orm(db_region_with_block_storage_service)
    validate_read_region_attrs(
        obj_out=schema, db_item=db_region_with_block_storage_service
    )
    schema = RegionReadPublic.from_orm(db_region_with_block_storage_service)
    validate_read_public_region_attrs(
        obj_out=schema, db_item=db_region_with_block_storage_service
    )
    schema = RegionReadExtended.from_orm(db_region_with_block_storage_service)
    validate_read_extended_region_attrs(
        obj_out=schema, db_item=db_region_with_block_storage_service
    )
    schema = RegionReadExtendedPublic.from_orm(db_region_with_block_storage_service)
    validate_read_extended_public_region_attrs(
        obj_out=schema, db_item=db_region_with_block_storage_service
    )


def test_read_schema_with_single_compute_service(
    db_region_with_compute_service: Region,
):
    """Create a valid 'Read' from DB object.

    Apply conversion for this item for all read schemas. No one of them should raise
    errors.

    Target region has a block storage service.
    """
    schema = RegionRead.from_orm(db_region_with_compute_service)
    validate_read_region_attrs(obj_out=schema, db_item=db_region_with_compute_service)
    schema = RegionReadPublic.from_orm(db_region_with_compute_service)
    validate_read_public_region_attrs(
        obj_out=schema, db_item=db_region_with_compute_service
    )
    schema = RegionReadExtended.from_orm(db_region_with_compute_service)
    validate_read_extended_region_attrs(
        obj_out=schema, db_item=db_region_with_compute_service
    )
    schema = RegionReadExtendedPublic.from_orm(db_region_with_compute_service)
    validate_read_extended_public_region_attrs(
        obj_out=schema, db_item=db_region_with_compute_service
    )


def test_read_schema_with_single_identity_service(
    db_region_with_identity_service: Region,
):
    """Create a valid 'Read' from DB object.

    Apply conversion for this item for all read schemas. No one of them should raise
    errors.

    Target region has a block storage service.
    """
    schema = RegionRead.from_orm(db_region_with_identity_service)
    validate_read_region_attrs(obj_out=schema, db_item=db_region_with_identity_service)
    schema = RegionReadPublic.from_orm(db_region_with_identity_service)
    validate_read_public_region_attrs(
        obj_out=schema, db_item=db_region_with_identity_service
    )
    schema = RegionReadExtended.from_orm(db_region_with_identity_service)
    validate_read_extended_region_attrs(
        obj_out=schema, db_item=db_region_with_identity_service
    )
    schema = RegionReadExtendedPublic.from_orm(db_region_with_identity_service)
    validate_read_extended_public_region_attrs(
        obj_out=schema, db_item=db_region_with_identity_service
    )


def test_read_schema_with_single_network_service(
    db_region_with_network_service: Region,
):
    """Create a valid 'Read' from DB object.

    Apply conversion for this item for all read schemas. No one of them should raise
    errors.

    Target region has a block storage service.
    """
    schema = RegionRead.from_orm(db_region_with_network_service)
    validate_read_region_attrs(obj_out=schema, db_item=db_region_with_network_service)
    schema = RegionReadPublic.from_orm(db_region_with_network_service)
    validate_read_public_region_attrs(
        obj_out=schema, db_item=db_region_with_network_service
    )
    schema = RegionReadExtended.from_orm(db_region_with_network_service)
    validate_read_extended_region_attrs(
        obj_out=schema, db_item=db_region_with_network_service
    )
    schema = RegionReadExtendedPublic.from_orm(db_region_with_network_service)
    validate_read_extended_public_region_attrs(
        obj_out=schema, db_item=db_region_with_network_service
    )
