from uuid import uuid4

import pytest
from app.provider.models import Provider
from app.region.crud import region
from app.region.schemas import RegionRead, RegionReadPublic, RegionReadShort
from app.region.schemas_extended import RegionReadExtended, RegionReadExtendedPublic
from pydantic import ValidationError
from tests.utils.region import create_random_region


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


def test_read_schema(db_provider: Provider):
    """Create a valid 'Read' Schema."""
    obj_in = create_random_region()
    db_obj = region.create(obj_in=obj_in, provider=db_provider)
    RegionRead.from_orm(db_obj)
    RegionReadPublic.from_orm(db_obj)
    RegionReadShort.from_orm(db_obj)
    RegionReadExtended.from_orm(db_obj)
    RegionReadExtendedPublic.from_orm(db_obj)

    obj_in = create_random_region(default=True)
    db_obj = region.update(db_obj=db_obj, obj_in=obj_in, force=True)
    RegionRead.from_orm(db_obj)
    RegionReadPublic.from_orm(db_obj)
    RegionReadShort.from_orm(db_obj)
    RegionReadExtended.from_orm(db_obj)
    RegionReadExtendedPublic.from_orm(db_obj)

    obj_in = create_random_region(with_location=True)
    db_obj = region.update(db_obj=db_obj, obj_in=obj_in, force=True)
    RegionRead.from_orm(db_obj)
    RegionReadPublic.from_orm(db_obj)
    RegionReadShort.from_orm(db_obj)
    RegionReadExtended.from_orm(db_obj)
    RegionReadExtendedPublic.from_orm(db_obj)

    obj_in = create_random_region(default=True, with_location=True)
    db_obj = region.update(db_obj=db_obj, obj_in=obj_in, force=True)
    RegionRead.from_orm(db_obj)
    RegionReadPublic.from_orm(db_obj)
    RegionReadShort.from_orm(db_obj)
    RegionReadExtended.from_orm(db_obj)
    RegionReadExtendedPublic.from_orm(db_obj)

    obj_in = create_random_region(with_block_storage_services=True)
    db_obj = region.update(db_obj=db_obj, obj_in=obj_in, force=True)
    RegionRead.from_orm(db_obj)
    RegionReadPublic.from_orm(db_obj)
    RegionReadShort.from_orm(db_obj)
    RegionReadExtended.from_orm(db_obj)
    RegionReadExtendedPublic.from_orm(db_obj)

    obj_in = create_random_region(default=True, with_block_storage_services=True)
    db_obj = region.update(db_obj=db_obj, obj_in=obj_in, force=True)
    RegionRead.from_orm(db_obj)
    RegionReadPublic.from_orm(db_obj)
    RegionReadShort.from_orm(db_obj)
    RegionReadExtended.from_orm(db_obj)
    RegionReadExtendedPublic.from_orm(db_obj)

    obj_in = create_random_region(with_compute_services=True)
    db_obj = region.update(db_obj=db_obj, obj_in=obj_in, force=True)
    RegionRead.from_orm(db_obj)
    RegionReadPublic.from_orm(db_obj)
    RegionReadShort.from_orm(db_obj)
    RegionReadExtended.from_orm(db_obj)
    RegionReadExtendedPublic.from_orm(db_obj)

    obj_in = create_random_region(default=True, with_compute_services=True)
    db_obj = region.update(db_obj=db_obj, obj_in=obj_in, force=True)
    RegionRead.from_orm(db_obj)
    RegionReadPublic.from_orm(db_obj)
    RegionReadShort.from_orm(db_obj)
    RegionReadExtended.from_orm(db_obj)
    RegionReadExtendedPublic.from_orm(db_obj)

    obj_in = create_random_region(with_identity_services=True)
    db_obj = region.update(db_obj=db_obj, obj_in=obj_in, force=True)
    RegionRead.from_orm(db_obj)
    RegionReadPublic.from_orm(db_obj)
    RegionReadShort.from_orm(db_obj)
    RegionReadExtended.from_orm(db_obj)
    RegionReadExtendedPublic.from_orm(db_obj)

    obj_in = create_random_region(default=True, with_identity_services=True)
    db_obj = region.update(db_obj=db_obj, obj_in=obj_in, force=True)
    RegionRead.from_orm(db_obj)
    RegionReadPublic.from_orm(db_obj)
    RegionReadShort.from_orm(db_obj)
    RegionReadExtended.from_orm(db_obj)
    RegionReadExtendedPublic.from_orm(db_obj)

    obj_in = create_random_region(with_network_services=True)
    db_obj = region.update(db_obj=db_obj, obj_in=obj_in, force=True)
    RegionRead.from_orm(db_obj)
    RegionReadPublic.from_orm(db_obj)
    RegionReadShort.from_orm(db_obj)
    RegionReadExtended.from_orm(db_obj)
    RegionReadExtendedPublic.from_orm(db_obj)

    obj_in = create_random_region(default=True, with_network_services=True)
    db_obj = region.update(db_obj=db_obj, obj_in=obj_in, force=True)
    RegionRead.from_orm(db_obj)
    RegionReadPublic.from_orm(db_obj)
    RegionReadShort.from_orm(db_obj)
    RegionReadExtended.from_orm(db_obj)
    RegionReadExtendedPublic.from_orm(db_obj)

    obj_in = create_random_region(
        with_location=True,
        with_block_storage_services=True,
        with_compute_services=True,
        with_identity_services=True,
        with_network_services=True,
    )
    db_obj = region.update(db_obj=db_obj, obj_in=obj_in, force=True)
    RegionRead.from_orm(db_obj)
    RegionReadPublic.from_orm(db_obj)
    RegionReadShort.from_orm(db_obj)
    RegionReadExtended.from_orm(db_obj)
    RegionReadExtendedPublic.from_orm(db_obj)

    obj_in = create_random_region(
        default=True,
        with_location=True,
        with_block_storage_services=True,
        with_compute_services=True,
        with_identity_services=True,
        with_network_services=True,
    )
    db_obj = region.update(db_obj=db_obj, obj_in=obj_in, force=True)
    RegionRead.from_orm(db_obj)
    RegionReadPublic.from_orm(db_obj)
    RegionReadShort.from_orm(db_obj)
    RegionReadExtended.from_orm(db_obj)
    RegionReadExtendedPublic.from_orm(db_obj)

    obj_in = create_random_region(
        with_block_storage_services=True,
        projects=[i.uuid for i in db_provider.projects],
    )
    db_obj = region.update(
        db_obj=db_obj, obj_in=obj_in, projects=db_provider.projects, force=True
    )
    RegionRead.from_orm(db_obj)
    RegionReadPublic.from_orm(db_obj)
    RegionReadShort.from_orm(db_obj)
    RegionReadExtended.from_orm(db_obj)
    RegionReadExtendedPublic.from_orm(db_obj)

    obj_in = create_random_region(
        default=True,
        with_block_storage_services=True,
        projects=[i.uuid for i in db_provider.projects],
    )
    db_obj = region.update(
        db_obj=db_obj, obj_in=obj_in, projects=db_provider.projects, force=True
    )
    RegionRead.from_orm(db_obj)
    RegionReadPublic.from_orm(db_obj)
    RegionReadShort.from_orm(db_obj)
    RegionReadExtended.from_orm(db_obj)
    RegionReadExtendedPublic.from_orm(db_obj)

    obj_in = create_random_region(
        with_compute_services=True, projects=[i.uuid for i in db_provider.projects]
    )
    db_obj = region.update(
        db_obj=db_obj, obj_in=obj_in, projects=db_provider.projects, force=True
    )
    RegionRead.from_orm(db_obj)
    RegionReadPublic.from_orm(db_obj)
    RegionReadShort.from_orm(db_obj)
    RegionReadExtended.from_orm(db_obj)
    RegionReadExtendedPublic.from_orm(db_obj)

    obj_in = create_random_region(
        default=True,
        with_compute_services=True,
        projects=[i.uuid for i in db_provider.projects],
    )
    db_obj = region.update(
        db_obj=db_obj, obj_in=obj_in, projects=db_provider.projects, force=True
    )
    RegionRead.from_orm(db_obj)
    RegionReadPublic.from_orm(db_obj)
    RegionReadShort.from_orm(db_obj)
    RegionReadExtended.from_orm(db_obj)
    RegionReadExtendedPublic.from_orm(db_obj)

    obj_in = create_random_region(
        with_network_services=True, projects=[i.uuid for i in db_provider.projects]
    )
    db_obj = region.update(
        db_obj=db_obj, obj_in=obj_in, projects=db_provider.projects, force=True
    )
    RegionRead.from_orm(db_obj)
    RegionReadPublic.from_orm(db_obj)
    RegionReadShort.from_orm(db_obj)
    RegionReadExtended.from_orm(db_obj)
    RegionReadExtendedPublic.from_orm(db_obj)

    obj_in = create_random_region(
        default=True,
        with_network_services=True,
        projects=[i.uuid for i in db_provider.projects],
    )
    db_obj = region.update(
        db_obj=db_obj, obj_in=obj_in, projects=db_provider.projects, force=True
    )
    RegionRead.from_orm(db_obj)
    RegionReadPublic.from_orm(db_obj)
    RegionReadShort.from_orm(db_obj)
    RegionReadExtended.from_orm(db_obj)
    RegionReadExtendedPublic.from_orm(db_obj)

    obj_in = create_random_region(
        with_location=True,
        with_block_storage_services=True,
        with_compute_services=True,
        with_identity_services=True,
        with_network_services=True,
        projects=[i.uuid for i in db_provider.projects],
    )
    db_obj = region.update(
        db_obj=db_obj, obj_in=obj_in, projects=db_provider.projects, force=True
    )
    RegionRead.from_orm(db_obj)
    RegionReadPublic.from_orm(db_obj)
    RegionReadShort.from_orm(db_obj)
    RegionReadExtended.from_orm(db_obj)
    RegionReadExtendedPublic.from_orm(db_obj)

    obj_in = create_random_region(
        default=True,
        with_location=True,
        with_block_storage_services=True,
        with_compute_services=True,
        with_identity_services=True,
        with_network_services=True,
        projects=[i.uuid for i in db_provider.projects],
    )
    db_obj = region.update(
        db_obj=db_obj, obj_in=obj_in, projects=db_provider.projects, force=True
    )
    RegionRead.from_orm(db_obj)
    RegionReadPublic.from_orm(db_obj)
    RegionReadShort.from_orm(db_obj)
    RegionReadExtended.from_orm(db_obj)
    RegionReadExtendedPublic.from_orm(db_obj)
