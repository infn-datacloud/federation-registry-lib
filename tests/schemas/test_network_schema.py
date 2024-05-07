from random import randint
from typing import Any, Literal, Optional
from uuid import UUID, uuid4

import pytest
from pytest_cases import case, parametrize, parametrize_with_cases

from fed_reg.models import BaseNode, BaseNodeCreate, BaseNodeQuery, BaseNodeRead
from fed_reg.network.models import Network
from fed_reg.network.schemas import (
    NetworkBase,
    NetworkBasePublic,
    NetworkCreate,
    NetworkQuery,
    NetworkRead,
    NetworkReadPublic,
    NetworkUpdate,
)
from fed_reg.provider.schemas_extended import NetworkCreateExtended
from tests.create_dict import network_schema_dict
from tests.utils import random_lower_string


class CaseAttr:
    @case(tags=["base_public", "base", "update"])
    def case_none(self) -> tuple[None, None]:
        return None, None

    @case(tags=["base_public", "base"])
    def case_desc(self) -> tuple[Literal["description"], str]:
        return "description", random_lower_string()

    @case(tags=["base"])
    @parametrize(attr=["mtu"])
    def case_integer(self, attr: str) -> tuple[str, int]:
        return attr, randint(0, 100)

    @case(tags=["base"])
    @parametrize(value=[True, False])
    @parametrize(attr=["is_shared", "is_router_external", "is_default"])
    def case_boolean(self, attr: str, value: bool) -> tuple[str, bool]:
        return attr, value

    @case(tags=["base"])
    @parametrize(attr=["proxy_host", "proxy_user"])
    def case_string(self, attr: str) -> tuple[str, str]:
        return attr, random_lower_string()

    @case(tags=["base"])
    @parametrize(len=[0, 1, 2])
    def case_tag_list(self, len: int) -> tuple[Literal["tags"], Optional[list[str]]]:
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
    @case(tags=["base_public", "base", "update"])
    @parametrize(attr=["name", "uuid"])
    def case_attr(self, attr: str) -> tuple[str, None]:
        return attr, None

    @case(tags=["base"])
    @parametrize(attr=["mtu"])
    def case_integer(self, attr: str) -> tuple[str, Literal[-1]]:
        return attr, -1

    @case(tags=["create_extended"])
    @parametrize(with_project=[True, False])
    def case_project(self, with_project: bool) -> tuple[Optional[UUID], str]:
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


@parametrize_with_cases("key, value", cases=CaseAttr, has_tag=["base"])
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
    assert item.proxy_host == d.get("proxy_host")
    assert item.proxy_user == d.get("proxy_user")
    assert item.tags == d.get("tags", [])


@parametrize_with_cases("key, value", cases=CaseInvalidAttr, has_tag=["base"])
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


@parametrize_with_cases("key, value", cases=CaseAttr, has_tag=["base_public"])
def test_read_public(network_model: Network, key: str, value: str) -> None:
    assert issubclass(NetworkReadPublic, NetworkBasePublic)
    assert issubclass(NetworkReadPublic, BaseNodeRead)
    assert NetworkReadPublic.__config__.orm_mode

    if key:
        network_model.__setattr__(key, value)
    item = NetworkReadPublic.from_orm(network_model)

    assert item.uid
    assert item.uid == network_model.uid
    assert item.description == network_model.description
    assert item.name == network_model.name
    assert item.uuid == network_model.uuid


@parametrize_with_cases("key, value", cases=CaseInvalidAttr, has_tag=["base_public"])
def test_invalid_read_public(network_model: Network, key: str, value: str) -> None:
    network_model.__setattr__(key, value)
    with pytest.raises(ValueError):
        NetworkReadPublic.from_orm(network_model)


@parametrize_with_cases("key, value", cases=CaseAttr, has_tag=["base"])
def test_read(network_model: Network, key: str, value: Any) -> None:
    assert issubclass(NetworkRead, NetworkBase)
    assert issubclass(NetworkRead, BaseNodeRead)
    assert NetworkRead.__config__.orm_mode

    if key:
        network_model.__setattr__(key, value)
    item = NetworkRead.from_orm(network_model)

    assert item.uid
    assert item.uid == network_model.uid
    assert item.description == network_model.description
    assert item.name == network_model.name
    assert item.uuid == network_model.uuid
    assert item.is_shared == network_model.is_shared
    assert item.is_router_external == network_model.is_router_external
    assert item.is_default == network_model.is_default
    assert item.mtu == network_model.mtu
    assert item.proxy_host == network_model.proxy_host
    assert item.proxy_user == network_model.proxy_user
    assert item.tags == network_model.tags


@parametrize_with_cases("key, value", cases=CaseInvalidAttr, has_tag=["base"])
def test_invalid_read(network_model: Network, key: str, value: str) -> None:
    network_model.__setattr__(key, value)
    with pytest.raises(ValueError):
        NetworkRead.from_orm(network_model)


# TODO Test read extended classes
