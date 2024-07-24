from typing import Any, Optional
from uuid import UUID

from pytest_cases import parametrize_with_cases

from fed_reg.network.models import Network
from fed_reg.network.schemas import (
    NetworkBase,
    NetworkBasePublic,
    NetworkRead,
    NetworkReadPublic,
    NetworkUpdate,
)
from fed_reg.provider.schemas_extended import NetworkCreateExtended
from tests.create_dict import network_schema_dict


@parametrize_with_cases("key, value", has_tag="base_public")
def test_base_public(key: str, value: str) -> None:
    d = network_schema_dict()
    if key:
        d[key] = value
    item = NetworkBasePublic(**d)
    assert item.description == d.get("description", "")
    assert item.name == d.get("name")
    assert item.uuid == d.get("uuid").hex


@parametrize_with_cases("key, value", has_tag="base")
def test_base(key: str, value: Any) -> None:
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


@parametrize_with_cases("key, value", has_tag="update")
def test_update(key: str, value: Any) -> None:
    d = network_schema_dict()
    if key:
        d[key] = value
    item = NetworkUpdate(**d)
    assert item.name == d.get("name")
    assert item.uuid == (d.get("uuid").hex if d.get("uuid") else None)


@parametrize_with_cases("key, value", has_tag="base_public")
def test_read_public(network_model: Network, key: str, value: str) -> None:
    if key:
        network_model.__setattr__(key, value)
    item = NetworkReadPublic.from_orm(network_model)

    assert item.uid
    assert item.uid == network_model.uid
    assert item.description == network_model.description
    assert item.name == network_model.name
    assert item.uuid == network_model.uuid


@parametrize_with_cases("key, value", has_tag="base")
def test_read(network_model: Network, key: str, value: Any) -> None:
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


@parametrize_with_cases("project", has_tag="create_extended")
def test_create_extended(project: Optional[UUID]) -> None:
    d = network_schema_dict()
    d["is_shared"] = project is None
    d["project"] = project
    item = NetworkCreateExtended(**d)
    assert item.project == (d.get("project").hex if d.get("project") else None)


# TODO Test read extended classes
