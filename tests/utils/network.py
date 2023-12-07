from typing import Optional, Union
from uuid import uuid4

from app.network.models import Network
from app.network.schemas import (
    NetworkBase,
    NetworkRead,
    NetworkReadPublic,
    NetworkUpdate,
)
from app.network.schemas_extended import (
    NetworkReadExtended,
    NetworkReadExtendedPublic,
)
from app.provider.schemas_extended import NetworkCreateExtended
from tests.utils.utils import (
    random_bool,
    random_lower_string,
    random_non_negative_int,
)


def create_random_network(
    *, default: bool = False, project: Optional[str] = None
) -> NetworkCreateExtended:
    name = random_lower_string()
    uuid = uuid4()
    kwargs = {}
    if not default:
        kwargs = {
            "description": random_lower_string(),
            "is_shared": project is None,
            "is_router_external": random_bool(),
            "is_default": random_bool(),
            "mtu": random_non_negative_int(),
            "proxy_ip": random_lower_string(),
            "proxy_user": random_non_negative_int(),
            "tags": [random_lower_string()],
        }
        if project:
            kwargs["project"] = project
    return NetworkCreateExtended(name=name, uuid=uuid, **kwargs)


def create_random_network_patch(default: bool = False) -> NetworkUpdate:
    if default:
        return NetworkUpdate()
    description = random_lower_string()
    name = random_lower_string()
    uuid = uuid4()
    is_shared = random_bool()
    is_router_external = random_bool()
    is_default = random_bool()
    mtu = random_non_negative_int()
    proxy_ip = random_lower_string()
    proxy_user = random_non_negative_int()
    tags = [random_lower_string()]
    return NetworkUpdate(
        description=description,
        name=name,
        uuid=uuid,
        is_shared=is_shared,
        is_router_external=is_router_external,
        is_default=is_default,
        mtu=mtu,
        proxy_ip=proxy_ip,
        proxy_user=proxy_user,
        tags=tags,
    )


def validate_public_attrs(*, obj_in: NetworkBase, db_item: Network) -> None:
    assert db_item.description == obj_in.description
    assert db_item.name == obj_in.name
    assert db_item.uuid == obj_in.uuid
    assert db_item.is_shared == obj_in.is_shared
    assert db_item.is_router_external == obj_in.is_router_external
    assert db_item.is_default == obj_in.is_default
    assert db_item.mtu == obj_in.mtu
    assert db_item.proxy_ip == obj_in.proxy_ip
    assert db_item.proxy_user == obj_in.proxy_user
    assert db_item.tags == obj_in.tags


def validate_attrs(*, obj_in: NetworkBase, db_item: Network) -> None:
    validate_public_attrs(obj_in=obj_in, db_item=db_item)


def validate_rels(
    *,
    obj_out: Union[NetworkReadExtended, NetworkReadExtendedPublic],
    db_item: Network,
) -> None:
    db_service = db_item.service.single()
    assert db_service
    assert db_service.uid == obj_out.service.uid
    db_project = db_item.project.single()
    if db_project:
        assert db_project.uid == obj_out.project.uid
    else:
        assert not obj_out.project


def validate_create_network_attrs(
    *, obj_in: NetworkCreateExtended, db_item: Network
) -> None:
    validate_attrs(obj_in=obj_in, db_item=db_item)
    db_project = db_item.project.single()
    if db_project:
        assert db_project.uuid == obj_in.project
    else:
        assert not obj_in.project


def validate_read_network_attrs(*, obj_out: NetworkRead, db_item: Network) -> None:
    assert db_item.uid == obj_out.uid
    validate_attrs(obj_in=obj_out, db_item=db_item)


def validate_read_public_network_attrs(
    *, obj_out: NetworkReadPublic, db_item: Network
) -> None:
    assert db_item.uid == obj_out.uid
    validate_public_attrs(obj_in=obj_out, db_item=db_item)


def validate_read_extended_network_attrs(
    *, obj_out: NetworkReadExtended, db_item: Network
) -> None:
    assert db_item.uid == obj_out.uid
    validate_attrs(obj_in=obj_out, db_item=db_item)
    validate_rels(obj_out=obj_out, db_item=db_item)


def validate_read_extended_public_network_attrs(
    *, obj_out: NetworkReadExtendedPublic, db_item: Network
) -> None:
    assert db_item.uid == obj_out.uid
    validate_public_attrs(obj_in=obj_out, db_item=db_item)
    validate_rels(obj_out=obj_out, db_item=db_item)
