from typing import Any
from uuid import UUID

from pytest_cases import parametrize_with_cases

from fed_reg.flavor.models import Flavor
from fed_reg.flavor.schemas import (
    FlavorBase,
    FlavorBasePublic,
    FlavorRead,
    FlavorReadPublic,
    FlavorUpdate,
)
from fed_reg.provider.schemas_extended import FlavorCreateExtended
from tests.create_dict import flavor_schema_dict


@parametrize_with_cases("key, value", has_tag="base_public")
def test_base_public(key: str, value: str) -> None:
    d = flavor_schema_dict()
    if key:
        d[key] = value
    item = FlavorBasePublic(**d)
    assert item.description == d.get("description", "")
    assert item.name == d.get("name")
    assert item.uuid == d.get("uuid").hex


@parametrize_with_cases("key, value", has_tag="base")
def test_base(key: str, value: Any) -> None:
    d = flavor_schema_dict()
    if key:
        d[key] = value
        if key.startswith("gpu_"):
            d["gpus"] = 1
    item = FlavorBase(**d)
    assert item.name == d.get("name")
    assert item.uuid == d.get("uuid").hex
    assert item.disk == d.get("disk", 0)
    assert item.ram == d.get("ram", 0)
    assert item.vcpus == d.get("vcpus", 0)
    assert item.swap == d.get("swap", 0)
    assert item.ephemeral == d.get("ephemeral", 0)
    assert item.gpus == d.get("gpus", 0)
    assert item.is_public == d.get("is_public", True)
    assert item.infiniband == d.get("infiniband", False)
    assert item.gpu_model == d.get("gpu_model")
    assert item.gpu_vendor == d.get("gpu_vendor")
    assert item.local_storage == d.get("local_storage")


@parametrize_with_cases("key, value", has_tag="update")
def test_update(key: str, value: Any) -> None:
    d = flavor_schema_dict()
    if key:
        d[key] = value
    item = FlavorUpdate(**d)
    assert item.name == d.get("name")
    assert item.uuid == (d.get("uuid").hex if d.get("uuid") else None)


@parametrize_with_cases("projects", has_tag="create_extended")
def test_create_extended(projects: list[UUID]) -> None:
    d = flavor_schema_dict()
    d["is_public"] = len(projects) == 0
    d["projects"] = projects
    item = FlavorCreateExtended(**d)
    assert item.projects == [i.hex for i in projects]


@parametrize_with_cases("key, value", has_tag="base_public")
def test_read_public(flavor_model: Flavor, key: str, value: str) -> None:
    if key:
        flavor_model.__setattr__(key, value)
    item = FlavorReadPublic.from_orm(flavor_model)

    assert item.uid
    assert item.uid == flavor_model.uid
    assert item.description == flavor_model.description
    assert item.name == flavor_model.name
    assert item.uuid == flavor_model.uuid


@parametrize_with_cases("key, value", has_tag="base")
def test_read(flavor_model: Flavor, key: str, value: Any) -> None:
    if key:
        flavor_model.__setattr__(key, value)
        if key.startswith("gpu_"):
            flavor_model.__setattr__("gpus", 1)
    item = FlavorRead.from_orm(flavor_model)

    assert item.uid
    assert item.uid == flavor_model.uid
    assert item.description == flavor_model.description
    assert item.name == flavor_model.name
    assert item.uuid == flavor_model.uuid
    assert item.disk == flavor_model.disk
    assert item.ram == flavor_model.ram
    assert item.vcpus == flavor_model.vcpus
    assert item.swap == flavor_model.swap
    assert item.ephemeral == flavor_model.ephemeral
    assert item.gpus == flavor_model.gpus
    assert item.is_public == flavor_model.is_public
    assert item.infiniband == flavor_model.infiniband
    assert item.gpu_model == flavor_model.gpu_model
    assert item.gpu_vendor == flavor_model.gpu_vendor
    assert item.local_storage == flavor_model.local_storage


# TODO Test read extended classes
