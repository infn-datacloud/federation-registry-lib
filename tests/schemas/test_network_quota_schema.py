from random import randint
from typing import Any, Literal, Tuple
from uuid import uuid4

import pytest
from pytest_cases import case, parametrize, parametrize_with_cases

from fed_reg.models import BaseNodeCreate, BaseNodeQuery
from fed_reg.provider.schemas_extended import NetworkQuotaCreateExtended
from fed_reg.quota.enum import QuotaType
from fed_reg.quota.schemas import (
    NetworkQuotaBase,
    NetworkQuotaCreate,
    NetworkQuotaQuery,
    NetworkQuotaUpdate,
    QuotaBase,
)
from tests.utils import random_lower_string


class CaseAttr:
    @case(tags=["update"])
    def case_none(self) -> Tuple[None, None]:
        return None, None

    def case_desc(self) -> Tuple[Literal["description"], str]:
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
    def case_integer(self, attr: str, value: int) -> Tuple[str, int]:
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
    def case_integer(self, attr: str) -> Tuple[str, int]:
        return attr, randint(-100, -2)

    @parametrize(value=[i for i in QuotaType if i != QuotaType.NETWORK])
    def case_type(self, value: QuotaType) -> Tuple[Literal["type"], QuotaType]:
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


# TODO Test all read classes
