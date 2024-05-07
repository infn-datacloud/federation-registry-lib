from random import randint
from typing import Any, Literal
from uuid import uuid4

import pytest
from pytest_cases import case, parametrize, parametrize_with_cases

from fed_reg.models import BaseNodeCreate, BaseNodeQuery, BaseNodeRead
from fed_reg.provider.schemas_extended import NetworkQuotaCreateExtended
from fed_reg.quota.enum import QuotaType
from fed_reg.quota.models import NetworkQuota
from fed_reg.quota.schemas import (
    NetworkQuotaBase,
    NetworkQuotaCreate,
    NetworkQuotaQuery,
    NetworkQuotaRead,
    NetworkQuotaReadPublic,
    NetworkQuotaUpdate,
    QuotaBase,
)
from tests.utils import random_lower_string


class CaseAttr:
    @case(tags=["base_public", "update"])
    def case_none(self) -> tuple[None, None]:
        return None, None

    @case(tags=["base_public"])
    def case_desc(self) -> tuple[Literal["description"], str]:
        return "description", random_lower_string()

    @parametrize(value=[-1, randint(0, 100)])
    @parametrize(
        attr=[
            "public_ips",
            "networks",
            "ports",
            "security_groups",
            "security_group_rules",
        ]
    )
    def case_integer(self, attr: str, value: int) -> tuple[str, int]:
        return attr, value


class CaseInvalidAttr:
    @parametrize(
        attr=[
            "public_ips",
            "networks",
            "ports",
            "security_groups",
            "security_group_rules",
        ]
    )
    def case_integer(self, attr: str) -> tuple[str, int]:
        return attr, randint(-100, -2)

    @parametrize(value=[i for i in QuotaType if i != QuotaType.NETWORK])
    def case_type(self, value: QuotaType) -> tuple[Literal["type"], QuotaType]:
        return "type", value


@parametrize_with_cases("key, value", cases=CaseAttr)
def test_base(key: str, value: Any) -> None:
    assert issubclass(NetworkQuotaBase, QuotaBase)
    d = {key: value} if key else {}
    item = NetworkQuotaBase(**d)
    assert item.per_user == d.get("per_user", False)
    assert item.type == QuotaType.NETWORK.value
    assert item.public_ips == d.get("public_ips")
    assert item.networks == d.get("networks")
    assert item.ports == d.get("ports")
    assert item.security_groups == d.get("security_groups")
    assert item.security_group_rules == d.get("security_group_rules")


@parametrize_with_cases("key, value", cases=CaseInvalidAttr)
def test_invalid_base(key: str, value: Any) -> None:
    d = {key: value}
    with pytest.raises(ValueError):
        NetworkQuotaBase(**d)


def test_create() -> None:
    assert issubclass(NetworkQuotaCreate, BaseNodeCreate)
    assert issubclass(NetworkQuotaCreate, NetworkQuotaBase)


@parametrize_with_cases(
    "key, value", cases=[CaseInvalidAttr, CaseAttr], has_tag=["update"]
)
def test_update(key: str, value: Any) -> None:
    assert issubclass(NetworkQuotaUpdate, BaseNodeCreate)
    assert issubclass(NetworkQuotaUpdate, NetworkQuotaBase)
    d = {key: value} if key else {}
    item = NetworkQuotaUpdate(**d)
    assert item.type == QuotaType.NETWORK.value


def test_query() -> None:
    assert issubclass(NetworkQuotaQuery, BaseNodeQuery)


def test_create_extended() -> None:
    assert issubclass(NetworkQuotaCreateExtended, NetworkQuotaCreate)
    d = {"project": uuid4()}
    item = NetworkQuotaCreateExtended(**d)
    assert item.project == d["project"].hex


def test_invalid_create_extended() -> None:
    d = {}
    with pytest.raises(ValueError):
        NetworkQuotaCreateExtended(**d)


@parametrize_with_cases("key, value", cases=CaseAttr, has_tag=["base_public"])
def test_read_public(network_quota_model: NetworkQuota, key: str, value: str) -> None:
    assert issubclass(NetworkQuotaReadPublic, QuotaBase)
    assert issubclass(NetworkQuotaReadPublic, BaseNodeRead)
    assert NetworkQuotaReadPublic.__config__.orm_mode

    if key:
        network_quota_model.__setattr__(key, value)
    item = NetworkQuotaReadPublic.from_orm(network_quota_model)

    assert item.uid
    assert item.uid == network_quota_model.uid
    assert item.description == network_quota_model.description
    assert item.per_user == network_quota_model.per_user


@parametrize_with_cases("key, value", cases=CaseAttr)
def test_read(network_quota_model: NetworkQuota, key: str, value: Any) -> None:
    assert issubclass(NetworkQuotaRead, NetworkQuotaBase)
    assert issubclass(NetworkQuotaRead, BaseNodeRead)
    assert NetworkQuotaRead.__config__.orm_mode

    if key:
        network_quota_model.__setattr__(key, value)
    item = NetworkQuotaRead.from_orm(network_quota_model)

    assert item.uid
    assert item.uid == network_quota_model.uid
    assert item.description == network_quota_model.description
    assert item.per_user == network_quota_model.per_user
    assert item.type == network_quota_model.type
    assert item.networks == network_quota_model.networks
    assert item.ports == network_quota_model.ports
    assert item.public_ips == network_quota_model.public_ips
    assert item.security_groups == network_quota_model.security_groups
    assert item.security_group_rules == network_quota_model.security_group_rules


@parametrize_with_cases("key, value", cases=CaseInvalidAttr)
def test_invalid_read(network_quota_model: NetworkQuota, key: str, value: str) -> None:
    network_quota_model.__setattr__(key, value)
    with pytest.raises(ValueError):
        NetworkQuotaRead.from_orm(network_quota_model)


# TODO Test read extended classes
