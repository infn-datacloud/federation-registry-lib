from random import randint
from typing import Any, Literal, Tuple

import pytest
from pytest_cases import case, parametrize, parametrize_with_cases

from fed_reg.flavor.schemas import (
    FlavorBase,
    FlavorBasePublic,
    FlavorCreate,
    FlavorQuery,
    FlavorUpdate,
)
from fed_reg.models import BaseNode, BaseNodeCreate, BaseNodeQuery
from tests.create_dict import flavor_schema_dict
from tests.utils import random_lower_string


class CaseAttr:
    @case(tags=["base_public", "update"])
    def case_none(self) -> Tuple[None, None]:
        return None, None

    @case(tags=["base_public"])
    def case_desc(self) -> Tuple[Literal["description"], str]:
        return "description", random_lower_string()

    @parametrize(attr=["disk", "ram", "vcpus", "swap", "ephemeral", "gpus"])
    def case_integer(self, attr: str) -> Tuple[str, int]:
        return attr, randint(0, 100)

    @parametrize(value=[True, False])
    @parametrize(attr=["is_public", "infiniband"])
    def case_boolean(self, attr: str, value: bool) -> Tuple[str, bool]:
        return attr, value

    @parametrize(attr=["gpu_model", "gpu_vendor", "local_storage"])
    def case_string(self, attr: str) -> Tuple[str, str]:
        return attr, random_lower_string()


class CaseInvalidAttr:
    @case(tags=["base_public", "update"])
    @parametrize(attr=["name", "uuid"])
    def case_attr(self, attr: str) -> Tuple[str, None]:
        return attr, None

    @parametrize(attr=["disk", "ram", "vcpus", "swap", "ephemeral", "gpus"])
    def case_integer(self, attr: str) -> Tuple[str, None]:
        return attr, -1

    @parametrize(attr=["gpu_model", "gpu_vendor"])
    def case_gpu_details(self, attr: str) -> Tuple[str, str]:
        return attr, random_lower_string()


@parametrize_with_cases("key, value", cases=CaseAttr, has_tag=["base_public"])
def test_base_public(key: str, value: str) -> None:
    assert issubclass(FlavorBasePublic, BaseNode)
    d = flavor_schema_dict()
    if key:
        d[key] = value
    item = FlavorBasePublic(**d)
    assert item.description == d.get("description", "")
    assert item.name == d.get("name")
    assert item.uuid == d.get("uuid").hex


@parametrize_with_cases("key, value", cases=CaseInvalidAttr, has_tag=["base_public"])
def test_invalid_base_public(key: str, value: None) -> None:
    d = flavor_schema_dict()
    d[key] = value
    with pytest.raises(ValueError):
        FlavorBasePublic(**d)


@parametrize_with_cases("key, value", cases=CaseAttr)
def test_base(key: str, value: Any) -> None:
    assert issubclass(FlavorBase, FlavorBasePublic)
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


@parametrize_with_cases("key, value", cases=CaseInvalidAttr)
def test_invalid_base(key: str, value: Any) -> None:
    d = flavor_schema_dict()
    d[key] = value
    with pytest.raises(ValueError):
        FlavorBase(**d)


def test_create() -> None:
    assert issubclass(FlavorCreate, BaseNodeCreate)
    assert issubclass(FlavorCreate, FlavorBase)


@parametrize_with_cases(
    "key, value", cases=[CaseInvalidAttr, CaseAttr], has_tag=["update"]
)
def test_update(key: str, value: Any) -> None:
    assert issubclass(FlavorUpdate, BaseNodeCreate)
    assert issubclass(FlavorUpdate, FlavorBase)
    d = flavor_schema_dict()
    if key:
        d[key] = value
    item = FlavorUpdate(**d)
    assert item.name == d.get("name")
    assert item.uuid == (d.get("uuid").hex if d.get("uuid") else None)


def test_query() -> None:
    assert issubclass(FlavorQuery, BaseNodeQuery)


# TODO Test all read classes
