from typing import Any, Literal, Tuple

import pytest
from pytest_cases import case, parametrize_with_cases

from fed_reg.models import BaseNode, BaseNodeCreate, BaseNodeQuery
from fed_reg.region.schemas import (
    RegionBase,
    RegionBasePublic,
    RegionCreate,
    RegionQuery,
    RegionUpdate,
)
from tests.create_dict import region_schema_dict
from tests.utils import random_lower_string


class CaseAttr:
    @case(tags=["base_public", "update"])
    def case_none(self) -> Tuple[None, None]:
        return None, None

    @case(tags=["base_public"])
    def case_desc(self) -> Tuple[Literal["description"], str]:
        return "description", random_lower_string()


class CaseInvalidAttr:
    @case(tags=["base_public", "update"])
    def case_attr(self) -> Tuple[Literal["name"], None]:
        return "name", None


@parametrize_with_cases("key, value", cases=CaseAttr, has_tag=["base_public"])
def test_base_public(key: str, value: str) -> None:
    assert issubclass(RegionBasePublic, BaseNode)
    d = region_schema_dict()
    if key:
        d[key] = value
    item = RegionBasePublic(**d)
    assert item.description == d.get("description", "")
    assert item.name == d.get("name")


@parametrize_with_cases("key, value", cases=CaseInvalidAttr, has_tag=["base_public"])
def test_invalid_base_public(key: str, value: None) -> None:
    d = region_schema_dict()
    d[key] = value
    with pytest.raises(ValueError):
        RegionBasePublic(**d)


@parametrize_with_cases("key, value", cases=CaseAttr)
def test_base(key: str, value: Any) -> None:
    assert issubclass(RegionBase, RegionBasePublic)
    d = region_schema_dict()
    if key:
        d[key] = value
    item = RegionBase(**d)
    assert item.name == d.get("name")


@parametrize_with_cases("key, value", cases=CaseInvalidAttr)
def test_invalid_base(key: str, value: Any) -> None:
    d = region_schema_dict()
    d[key] = value
    with pytest.raises(ValueError):
        RegionBase(**d)


def test_create() -> None:
    assert issubclass(RegionCreate, BaseNodeCreate)
    assert issubclass(RegionCreate, RegionBase)


@parametrize_with_cases(
    "key, value", cases=[CaseInvalidAttr, CaseAttr], has_tag=["update"]
)
def test_update(key: str, value: Any) -> None:
    assert issubclass(RegionUpdate, BaseNodeCreate)
    assert issubclass(RegionUpdate, RegionBase)
    d = region_schema_dict()
    if key:
        d[key] = value
    item = RegionUpdate(**d)
    assert item.name == d.get("name")


def test_query() -> None:
    assert issubclass(RegionQuery, BaseNodeQuery)


# TODO Test all read classes
