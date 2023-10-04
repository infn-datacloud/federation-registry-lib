from typing import List
from uuid import uuid4

from app.provider.schemas_extended import RegionCreateExtended
from app.region.models import Region
from app.region.schemas import RegionUpdate
from app.service.enum import ServiceType
from app.tests.utils.location import create_random_location, validate_location_attrs
from app.tests.utils.service import (
    create_random_block_storage_service,
    create_random_compute_service,
    create_random_identity_service,
    create_random_network_service,
    validate_block_storage_service_attrs,
    validate_compute_service_attrs,
    validate_identity_service_attrs,
    validate_network_service_attrs,
)
from app.tests.utils.utils import random_lower_string
from pydantic import UUID4


def create_random_region(
    default: bool = False,
    with_location: bool = False,
    with_block_storage_services: bool = False,
    with_compute_services: bool = False,
    with_identity_services: bool = False,
    with_network_services: bool = False,
    projects: List[UUID4] = [],
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


def create_random_update_region_data() -> RegionUpdate:
    description = random_lower_string()
    name = random_lower_string()
    uuid = uuid4()
    public_network_name = random_lower_string()
    private_network_name = random_lower_string()
    private_network_proxy_host = random_lower_string()
    private_network_proxy_user = random_lower_string()
    return RegionUpdate(
        description=description,
        name=name,
        uuid=uuid,
        public_network_name=public_network_name,
        private_network_name=private_network_name,
        private_network_proxy_host=private_network_proxy_host,
        private_network_proxy_user=private_network_proxy_user,
    )


def validate_region_attrs(*, obj_in: RegionCreateExtended, db_item: Region) -> None:
    assert db_item.description == obj_in.description
    assert db_item.name == obj_in.name
    if db_item.location.single():
        validate_location_attrs(
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
            validate_block_storage_service_attrs(obj_in=serv_in, db_item=db_serv)

        db_compute_services = list(
            filter(lambda x: x.type == ServiceType.COMPUTE.value, db_item.services)
        )
        assert len(db_compute_services) == len(obj_in.compute_services)
        for db_serv, serv_in in zip(db_compute_services, obj_in.compute_services):
            validate_compute_service_attrs(obj_in=serv_in, db_item=db_serv)

        db_identity_services = list(
            filter(lambda x: x.type == ServiceType.IDENTITY.value, db_item.services)
        )
        assert len(db_identity_services) == len(obj_in.identity_services)
        for db_serv, serv_in in zip(db_identity_services, obj_in.identity_services):
            validate_identity_service_attrs(obj_in=serv_in, db_item=db_serv)

        db_network_services = list(
            filter(lambda x: x.type == ServiceType.NETWORK.value, db_item.services)
        )
        assert len(db_network_services) == len(obj_in.network_services)
        for db_serv, serv_in in zip(db_network_services, obj_in.network_services):
            validate_network_service_attrs(obj_in=serv_in, db_item=db_serv)
