from typing import List
from uuid import uuid4

from app.flavor.models import Flavor
from app.flavor.schemas import (
    FlavorBase,
    FlavorRead,
    FlavorReadPublic,
    FlavorReadShort,
    FlavorUpdate,
)
from app.flavor.schemas_extended import FlavorReadExtended, FlavorReadExtendedPublic
from app.provider.schemas_extended import FlavorCreateExtended
from app.tests.utils.utils import (
    random_bool,
    random_lower_string,
    random_non_negative_int,
    random_positive_int,
)


def create_random_flavor(
    *, default: bool = False, projects: List[str] = []
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


def create_random_flavor_patch(default: bool = False) -> FlavorUpdate:
    if default:
        return FlavorUpdate()
    description = random_lower_string()
    name = random_lower_string()
    uuid = uuid4()
    disk = random_non_negative_int()
    is_public = random_bool()
    ram = random_non_negative_int()
    vcpus = random_non_negative_int()
    swap = random_non_negative_int()
    ephemeral = random_non_negative_int()
    infiniband_support = random_bool()
    gpus = random_positive_int()
    gpu_model = random_lower_string()
    gpu_vendor = random_lower_string()
    local_storage = random_lower_string()
    return FlavorUpdate(
        description=description,
        name=name,
        uuid=uuid,
        disk=disk,
        is_public=is_public,
        ram=ram,
        vcpus=vcpus,
        swap=swap,
        ephemeral=ephemeral,
        infiniband_support=infiniband_support,
        gpus=gpus,
        gpu_model=gpu_model,
        gpu_vendor=gpu_vendor,
        local_storage=local_storage,
    )


def validate_flavor_attrs(*, obj_in: FlavorBase, db_item: Flavor) -> None:
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


def validate_flavor_public_attrs(*, obj_in: FlavorBase, db_item: Flavor) -> None:
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


def validate_create_flavor_attrs(
    *, obj_in: FlavorCreateExtended, db_item: Flavor
) -> None:
    validate_flavor_attrs(obj_in=obj_in, db_item=db_item)
    assert len(db_item.projects) == len(obj_in.projects)
    for db_proj, proj_in in zip(db_item.projects, obj_in.projects):
        assert db_proj.uuid == proj_in


def validate_read_flavor_attrs(*, obj_out: FlavorRead, db_item: Flavor) -> None:
    assert db_item.uid == obj_out.uid
    validate_flavor_attrs(obj_in=obj_out, db_item=db_item)


def validate_read_short_flavor_attrs(
    *, obj_out: FlavorReadShort, db_item: Flavor
) -> None:
    assert db_item.uid == obj_out.uid
    validate_flavor_attrs(obj_in=obj_out, db_item=db_item)


def validate_read_public_flavor_attrs(
    *, obj_out: FlavorReadPublic, db_item: Flavor
) -> None:
    assert db_item.uid == obj_out.uid
    validate_flavor_public_attrs(obj_in=obj_out, db_item=db_item)


def validate_read_extended_flavor_attrs(
    *, obj_out: FlavorReadExtended, db_item: Flavor
) -> None:
    assert db_item.uid == obj_out.uid
    validate_flavor_attrs(obj_in=obj_out, db_item=db_item)

    assert len(db_item.projects) == len(obj_out.projects)
    for db_proj, proj_out in zip(db_item.projects, obj_out.projects):
        assert db_proj.uid == proj_out.uid
    assert len(db_item.services) == len(obj_out.services)
    for db_serv, serv_out in zip(db_item.services, obj_out.services):
        assert db_serv.uid == serv_out.uid


def validate_read_extended_public_flavor_attrs(
    *, obj_out: FlavorReadExtendedPublic, db_item: Flavor
) -> None:
    assert db_item.uid == obj_out.uid
    validate_flavor_public_attrs(obj_in=obj_out, db_item=db_item)

    assert len(db_item.projects) == len(obj_out.projects)
    for db_proj, proj_out in zip(db_item.projects, obj_out.projects):
        assert db_proj.uid == proj_out.uid
    assert len(db_item.services) == len(obj_out.services)
    for db_serv, serv_out in zip(db_item.services, obj_out.services):
        assert db_serv.uid == serv_out.uid
