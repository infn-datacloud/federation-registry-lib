from random import choice
from typing import List

from app.provider.schemas_extended import NetworkServiceCreateExtended
from app.service.enum import NetworkServiceName
from app.service.models import NetworkService
from app.service.schemas import (
    NetworkServiceBase,
    NetworkServiceRead,
    NetworkServiceReadPublic,
    NetworkServiceReadShort,
    NetworkServiceUpdate,
)
from app.service.schemas_extended import (
    NetworkServiceReadExtended,
    NetworkServiceReadExtendedPublic,
)
from tests.utils.network import create_random_network, validate_create_network_attrs
from tests.utils.utils import random_lower_string, random_url


def create_random_network_service(
    *, default: bool = False, with_networks: bool = False, projects: List[str] = []
) -> NetworkServiceCreateExtended:
    endpoint = random_url()
    name = random_network_service_name()
    kwargs = {}
    if not default:
        kwargs = {"description": random_lower_string()}
    if with_networks:
        project = None if len(projects) == 0 else projects[0]
        kwargs["networks"] = [create_random_network(project=project)]
    return NetworkServiceCreateExtended(endpoint=endpoint, name=name, **kwargs)


def create_random_network_service_patch(
    default: bool = False,
) -> NetworkServiceUpdate:
    if default:
        return NetworkServiceUpdate()
    description = random_lower_string()
    endpoint = random_url()
    name = random_network_service_name()
    return NetworkServiceUpdate(description=description, endpoint=endpoint, name=name)


def random_network_service_name() -> str:
    return choice([i.value for i in NetworkServiceName])


def validate_network_service_attrs(
    *, obj_in: NetworkServiceBase, db_item: NetworkService
) -> None:
    assert db_item.description == obj_in.description
    assert db_item.endpoint == obj_in.endpoint
    assert db_item.name == obj_in.name
    assert db_item.type == obj_in.type


def validate_network_service_public_attrs(
    *, obj_in: NetworkServiceBase, db_item: NetworkService
) -> None:
    assert db_item.description == obj_in.description
    assert db_item.endpoint == obj_in.endpoint
    assert db_item.name == obj_in.name
    assert db_item.type == obj_in.type


def validate_create_network_service_attrs(
    *, obj_in: NetworkServiceCreateExtended, db_item: NetworkService
) -> None:
    validate_network_service_attrs(obj_in=obj_in, db_item=db_item)
    assert len(db_item.networks) == len(obj_in.networks)
    for db_net, net_in in zip(db_item.networks, obj_in.networks):
        validate_create_network_attrs(db_item=db_net, obj_in=net_in)


def validate_read_network_service_attrs(
    *, obj_out: NetworkServiceRead, db_item: NetworkService
) -> None:
    assert db_item.uid == obj_out.uid
    validate_network_service_attrs(obj_in=obj_out, db_item=db_item)


def validate_read_short_network_service_attrs(
    *, obj_out: NetworkServiceReadShort, db_item: NetworkService
) -> None:
    assert db_item.uid == obj_out.uid
    validate_network_service_attrs(obj_in=obj_out, db_item=db_item)


def validate_read_public_network_service_attrs(
    *, obj_out: NetworkServiceReadPublic, db_item: NetworkService
) -> None:
    assert db_item.uid == obj_out.uid
    validate_network_service_public_attrs(obj_in=obj_out, db_item=db_item)


def validate_read_extended_network_service_attrs(
    *, obj_out: NetworkServiceReadExtended, db_item: NetworkService
) -> None:
    assert db_item.uid == obj_out.uid
    validate_network_service_attrs(obj_in=obj_out, db_item=db_item)
    assert len(db_item.networks) == len(obj_out.networks)
    for db_net, net_out in zip(db_item.networks, obj_out.networks):
        assert db_net.uid == net_out.uid
    db_region = db_item.region.single()
    assert db_region
    assert db_region.uid == obj_out.region.uid


def validate_read_extended_public_network_service_attrs(
    *, obj_out: NetworkServiceReadExtendedPublic, db_item: NetworkService
) -> None:
    assert db_item.uid == obj_out.uid
    validate_network_service_attrs(obj_in=obj_out, db_item=db_item)
    assert len(db_item.networks) == len(obj_out.networks)
    for db_net, net_out in zip(db_item.networks, obj_out.networks):
        assert db_net.uid == net_out.uid
    db_region = db_item.region.single()
    assert db_region
    assert db_region.uid == obj_out.region.uid
