from typing import List

from app.provider.schemas_extended import RegionCreateExtended
from app.region.models import Region
from app.region.schemas import (
    RegionBase,
    RegionRead,
    RegionReadPublic,
    RegionReadShort,
    RegionUpdate,
)
from app.region.schemas_extended import RegionReadExtended, RegionReadExtendedPublic
from app.service.enum import ServiceType
from tests.utils.block_storage_service import (
    create_random_block_storage_service,
    validate_create_block_storage_service_attrs,
)
from tests.utils.compute_service import (
    create_random_compute_service,
    validate_create_compute_service_attrs,
)
from tests.utils.identity_service import (
    create_random_identity_service,
    validate_create_identity_service_attrs,
)
from tests.utils.location import create_random_location, validate_create_location_attrs
from tests.utils.network_service import (
    create_random_network_service,
    validate_create_network_service_attrs,
)
from tests.utils.utils import random_lower_string


def create_random_region(
    default: bool = False,
    with_location: bool = False,
    with_block_storage_services: bool = False,
    with_compute_services: bool = False,
    with_identity_services: bool = False,
    with_network_services: bool = False,
    projects: List[str] = [],
) -> RegionCreateExtended:
    name = random_lower_string()
    kwargs = {}
    if not default:
        kwargs = {"description": random_lower_string()}
    if with_location:
        kwargs["location"] = create_random_location()
    if with_block_storage_services:
        kwargs["block_storage_services"] = [
            create_random_block_storage_service(projects=projects)
        ]
    if with_compute_services:
        kwargs["compute_services"] = [
            create_random_compute_service(
                projects=projects, with_flavors=True, with_images=True
            )
        ]
    if with_identity_services:
        kwargs["identity_services"] = [create_random_identity_service()]
    if with_network_services:
        kwargs["network_services"] = [
            create_random_network_service(projects=projects, with_networks=True)
        ]
    return RegionCreateExtended(name=name, **kwargs)


def create_random_region_patch(*, default: bool = False) -> RegionUpdate:
    if default:
        return RegionUpdate()
    description = random_lower_string()
    name = random_lower_string()
    return RegionUpdate(description=description, name=name)


def validate_region_attrs(*, obj_in: RegionBase, db_item: Region) -> None:
    assert db_item.description == obj_in.description
    assert db_item.name == obj_in.name


def validate_region_public_attrs(*, obj_in: RegionBase, db_item: Region) -> None:
    assert db_item.description == obj_in.description
    assert db_item.name == obj_in.name


def validate_create_region_attrs(
    *, obj_in: RegionCreateExtended, db_item: Region
) -> None:
    validate_region_attrs(obj_in=obj_in, db_item=db_item)
    if db_item.location.single():
        validate_create_location_attrs(
            obj_in=obj_in.location, db_item=db_item.location.single()
        )
    else:
        assert not obj_in.location
    if len(db_item.services) > 0:
        db_block_storage_services = list(
            filter(
                lambda x: x.type == ServiceType.BLOCK_STORAGE.value, db_item.services
            )
        )
        assert len(db_block_storage_services) == len(obj_in.block_storage_services)
        for db_serv, serv_in in zip(
            db_block_storage_services, obj_in.block_storage_services
        ):
            validate_create_block_storage_service_attrs(obj_in=serv_in, db_item=db_serv)

        db_compute_services = list(
            filter(lambda x: x.type == ServiceType.COMPUTE.value, db_item.services)
        )
        assert len(db_compute_services) == len(obj_in.compute_services)
        for db_serv, serv_in in zip(db_compute_services, obj_in.compute_services):
            validate_create_compute_service_attrs(obj_in=serv_in, db_item=db_serv)

        db_identity_services = list(
            filter(lambda x: x.type == ServiceType.IDENTITY.value, db_item.services)
        )
        assert len(db_identity_services) == len(obj_in.identity_services)
        for db_serv, serv_in in zip(db_identity_services, obj_in.identity_services):
            validate_create_identity_service_attrs(obj_in=serv_in, db_item=db_serv)

        db_network_services = list(
            filter(lambda x: x.type == ServiceType.NETWORK.value, db_item.services)
        )
        assert len(db_network_services) == len(obj_in.network_services)
        for db_serv, serv_in in zip(db_network_services, obj_in.network_services):
            validate_create_network_service_attrs(obj_in=serv_in, db_item=db_serv)


def validate_read_region_attrs(*, obj_out: RegionRead, db_item: Region) -> None:
    assert db_item.uid == obj_out.uid
    validate_region_attrs(obj_in=obj_out, db_item=db_item)


def validate_read_short_region_attrs(
    *, obj_out: RegionReadShort, db_item: Region
) -> None:
    assert db_item.uid == obj_out.uid
    validate_region_attrs(obj_in=obj_out, db_item=db_item)


def validate_read_public_region_attrs(
    *, obj_out: RegionReadPublic, db_item: Region
) -> None:
    assert db_item.uid == obj_out.uid
    validate_region_public_attrs(obj_in=obj_out, db_item=db_item)


def validate_read_extended_region_attrs(
    *, obj_out: RegionReadExtended, db_item: Region
) -> None:
    assert db_item.uid == obj_out.uid
    validate_region_attrs(obj_in=obj_out, db_item=db_item)
    db_provider = db_item.provider.single()
    assert db_provider
    assert db_provider.uid == obj_out.provider.uid
    db_location = db_item.location.single()
    if db_location:
        assert db_location.uid == obj_out.location.uid
    else:
        assert not obj_out.location
    assert len(db_item.services) == len(obj_out.services)


def validate_read_extended_public_region_attrs(
    *, obj_out: RegionReadExtendedPublic, db_item: Region
) -> None:
    assert db_item.uid == obj_out.uid
    validate_region_public_attrs(obj_in=obj_out, db_item=db_item)
    db_provider = db_item.provider.single()
    assert db_provider
    assert db_provider.uid == obj_out.provider.uid
    db_location = db_item.location.single()
    if db_location:
        assert db_location.uid == obj_out.location.uid
    else:
        assert not obj_out.location
    assert len(db_item.services) == len(obj_out.services)
