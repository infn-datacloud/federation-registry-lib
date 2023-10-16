from typing import Optional
from uuid import uuid4

from app.network.models import Network
from app.network.schemas import NetworkUpdate
from app.provider.schemas_extended import NetworkCreateExtended
from app.tests.utils.utils import (
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


def create_random_update_network_data() -> NetworkUpdate:
    description = random_lower_string()
    name = random_lower_string()
    uuid = uuid4()
    num_vcpus = random_non_negative_int()
    num_gpus = random_non_negative_int()
    ram = random_non_negative_int()
    disk = random_non_negative_int()
    infiniband_support = random_bool()
    gpu_model = random_lower_string()
    gpu_vendor = random_lower_string()
    return NetworkUpdate(
        description=description,
        name=name,
        uuid=uuid,
        num_vcpus=num_vcpus,
        num_gpus=num_gpus,
        ram=ram,
        disk=disk,
        infiniband_support=infiniband_support,
        gpu_model=gpu_model,
        gpu_vendor=gpu_vendor,
    )


def validate_network_attrs(*, obj_in: NetworkCreateExtended, db_item: Network) -> None:
    assert db_item.description == obj_in.description
    assert db_item.name == obj_in.name
    assert db_item.uuid == str(obj_in.uuid)
    assert db_item.is_shared == obj_in.is_shared
    assert db_item.is_router_external == obj_in.is_router_external
    assert db_item.is_default == obj_in.is_default
    assert db_item.mtu == obj_in.mtu
    assert db_item.proxy_ip == obj_in.proxy_ip
    assert db_item.proxy_user == obj_in.proxy_user
    assert db_item.tags == obj_in.tags
    if db_item.project.single():
        assert db_item.project.single().uuid == str(obj_in.project)
    else:
        assert not obj_in.project
