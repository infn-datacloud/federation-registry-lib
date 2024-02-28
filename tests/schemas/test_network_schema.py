from random import randint
from typing import Any, List, Literal, Optional, Tuple
from uuid import UUID, uuid4

import pytest
from pytest_cases import case, parametrize, parametrize_with_cases

from fed_reg.models import BaseNode, BaseNodeCreate, BaseNodeQuery
from fed_reg.network.schemas import (
    NetworkBase,
    NetworkBasePublic,
    NetworkCreate,
    NetworkQuery,
    NetworkUpdate,
)
from fed_reg.provider.schemas_extended import NetworkCreateExtended
from tests.create_dict import network_schema_dict
from tests.utils import random_lower_string


class CaseAttr:
    @case(tags=["base_public", "update"])
    def case_none(self) -> Tuple[None, None]:
        return None, None

    @case(tags=["base_public"])
    def case_desc(self) -> Tuple[Literal["description"], str]:
        return "description", random_lower_string()

    @parametrize(attr=["mtu"])
    def case_integer(self, attr: str) -> Tuple[str, int]:
        return attr, randint(0, 100)

    @parametrize(value=[True, False])
    @parametrize(attr=["is_shared", "is_router_external", "is_default"])
    def case_boolean(self, attr: str, value: bool) -> Tuple[str, bool]:
        return attr, value

    @parametrize(attr=["proxy_ip", "proxy_user"])
    def case_string(self, attr: str) -> Tuple[str, str]:
        return attr, random_lower_string()

    @parametrize(len=[0, 1, 2])
    def case_tag_list(self, len: int) -> Tuple[Literal["tags"], Optional[List[str]]]:
        attr = "tags"
        if len == 0:
            return attr, []
        elif len == 1:
            return attr, [random_lower_string()]
        else:
            return attr, [random_lower_string() for _ in range(len)]

    @case(tags=["create_extended"])
    @parametrize(with_project=[True, False])
    def case_project(self, with_project: bool) -> Optional[UUID]:
        return uuid4() if with_project else None


class CaseInvalidAttr:
    @case(tags=["base_public", "update"])
    @parametrize(attr=["name", "uuid"])
    def case_attr(self, attr: str) -> Tuple[str, None]:
        return attr, None

    @parametrize(attr=["mtu"])
    def case_integer(self, attr: str) -> Tuple[str, Literal[-1]]:
        return attr, -1

    @case(tags=["create_extended"])
    @parametrize(with_project=[True, False])
    def case_project(self, with_project: bool) -> Tuple[Optional[UUID], str]:
        if with_project:
            return uuid4(), "Shared networks do not have a linked project"
        else:
            return None, "Projects is mandatory for private networks"


@parametrize_with_cases("key, value", cases=CaseAttr, has_tag=["base_public"])
def test_base_public(key: str, value: str) -> None:
    assert issubclass(NetworkBasePublic, BaseNode)
    d = network_schema_dict()
    if key:
        d[key] = value
    item = NetworkBasePublic(**d)
    assert item.description == d.get("description", "")
    assert item.name == d.get("name")
    assert item.uuid == d.get("uuid").hex


@parametrize_with_cases("key, value", cases=CaseInvalidAttr, has_tag=["base_public"])
def test_invalid_base_public(key: str, value: None) -> None:
    d = network_schema_dict()
    d[key] = value
    with pytest.raises(ValueError):
        NetworkBasePublic(**d)


@parametrize_with_cases(
    "key, value", cases=CaseAttr, filter=lambda f: not f.has_tag("create_extended")
)
def test_base(key: str, value: Any) -> None:
    assert issubclass(NetworkBase, NetworkBasePublic)
    d = network_schema_dict()
    if key:
        d[key] = value
    item = NetworkBase(**d)
    assert item.name == d.get("name")
    assert item.uuid == d.get("uuid").hex
    assert item.is_shared == d.get("is_shared", True)
    assert item.is_router_external == d.get("is_router_external", False)
    assert item.is_default == d.get("is_default", False)
    assert item.mtu == d.get("mtu")
    assert item.proxy_ip == d.get("proxy_ip")
    assert item.proxy_user == d.get("proxy_user")
    assert item.tags == d.get("tags", [])


@parametrize_with_cases(
    "key, value",
    cases=CaseInvalidAttr,
    filter=lambda f: not f.has_tag("create_extended"),
)
def test_invalid_base(key: str, value: Any) -> None:
    d = network_schema_dict()
    d[key] = value
    with pytest.raises(ValueError):
        NetworkBase(**d)


def test_create() -> None:
    assert issubclass(NetworkCreate, BaseNodeCreate)
    assert issubclass(NetworkCreate, NetworkBase)


@parametrize_with_cases(
    "key, value", cases=[CaseInvalidAttr, CaseAttr], has_tag=["update"]
)
def test_update(key: str, value: Any) -> None:
    assert issubclass(NetworkUpdate, BaseNodeCreate)
    assert issubclass(NetworkUpdate, NetworkBase)
    d = network_schema_dict()
    if key:
        d[key] = value
    item = NetworkUpdate(**d)
    assert item.name == d.get("name")
    assert item.uuid == (d.get("uuid").hex if d.get("uuid") else None)


def test_query() -> None:
    assert issubclass(NetworkQuery, BaseNodeQuery)


@parametrize_with_cases("project", cases=CaseAttr, has_tag=["create_extended"])
def test_create_extended(project: Optional[UUID]) -> None:
    assert issubclass(NetworkCreateExtended, NetworkCreate)
    d = network_schema_dict()
    d["is_shared"] = project is None
    d["project"] = project
    item = NetworkCreateExtended(**d)
    assert item.project == (d.get("project").hex if d.get("project") else None)


@parametrize_with_cases(
    "project, msg", cases=CaseInvalidAttr, has_tag=["create_extended"]
)
def test_invalid_create_extended(project: Optional[UUID], msg: str) -> None:
    d = network_schema_dict()
    d["is_shared"] = project is not None
    d["project"] = project
    with pytest.raises(ValueError, match=msg):
        NetworkCreateExtended(**d)


# TODO Test all read classes
