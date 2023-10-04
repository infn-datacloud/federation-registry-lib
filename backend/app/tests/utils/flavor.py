from typing import List
from uuid import uuid4

from app.flavor.models import Flavor
from app.flavor.schemas import FlavorUpdate
from app.provider.schemas_extended import FlavorCreateExtended
from app.tests.utils.utils import (
    random_bool,
    random_lower_string,
    random_non_negative_int,
    random_positive_int,
)
from pydantic import UUID4


def create_random_flavor(
    *, default: bool = False, projects: List[UUID4] = []
) -> FlavorCreateExtended:
    name = random_lower_string()
    uuid = uuid4()
    kwargs = {}
    if not default:
        kwargs = {
            "description": random_lower_string(),
            "disk": random_non_negative_int(),
            "is_public": len(projects) == 0,
            "ram": random_non_negative_int(),
            "vcpus": random_non_negative_int(),
            "swap": random_non_negative_int(),
            "ephemeral": random_non_negative_int(),
            "infiniband_support": random_bool(),
            "gpus": random_positive_int(),
            "gpu_model": random_lower_string(),
            "gpu_vendor": random_lower_string(),
            "local_storage": random_lower_string(),
        }
        if len(projects) > 0:
            kwargs["projects"] = projects
    return FlavorCreateExtended(name=name, uuid=uuid, **kwargs)


def create_random_update_flavor_data() -> FlavorUpdate:
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
    return FlavorUpdate(
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


def validate_flavor_attrs(*, obj_in: FlavorCreateExtended, db_item: Flavor) -> None:
    assert db_item.description == obj_in.description
    assert db_item.name == obj_in.name
    assert db_item.uuid == obj_in.uuid
    assert db_item.disk == obj_in.disk
    assert db_item.is_public == obj_in.is_public
    assert db_item.ram == obj_in.ram
    assert db_item.vcpus == obj_in.vcpus
    assert db_item.swap == obj_in.swap
    assert db_item.ephemeral == obj_in.ephemeral
    assert db_item.infiniband == obj_in.infiniband
    assert db_item.gpus == obj_in.gpus
    assert db_item.gpu_model == obj_in.gpu_model
    assert db_item.gpu_vendor == obj_in.gpu_vendor
    assert db_item.local_storage == obj_in.local_storage
    assert len(db_item.projects) == len(obj_in.projects)
    for db_proj, proj_in in zip(db_item.projects, obj_in.projects):
        assert db_proj == proj_in
