from random import randint
from typing import Any, Literal, Tuple

import pytest
from pytest_cases import case, parametrize, parametrize_with_cases

from fed_reg.models import BaseNodeCreate, BaseNodeQuery
from fed_reg.quota.enum import QuotaType
from fed_reg.quota.schemas import (
    ComputeQuotaBase,
    ComputeQuotaCreate,
    ComputeQuotaQuery,
    ComputeQuotaUpdate,
    QuotaBase,
)
from tests.utils import random_lower_string


class CaseAttr:
    @case(tags=["update"])
    def case_none(self) -> Tuple[None, None]:
        return None, None

    def case_desc(self) -> Tuple[Literal["description"], str]:
        return "description", random_lower_string()

    @parametrize(attr=["cores", "instances", "ram"])
    def case_integer(self, attr: str) -> Tuple[str, int]:
        return attr, randint(0, 100)


class CaseInvalidAttr:
    @parametrize(attr=["cores", "instances", "ram"])
    def case_integer(self, attr: str) -> Tuple[str, Literal[-1]]:
        return attr, -1

    @parametrize(value=[i for i in QuotaType if i != QuotaType.COMPUTE])
    def case_type(self, value: QuotaType) -> Tuple[Literal["type"], QuotaType]:
        return "type", value


@parametrize_with_cases("key, value", cases=CaseAttr)
def test_base(key: str, value: Any) -> None:
    assert issubclass(ComputeQuotaBase, QuotaBase)
    d = {key: value} if key else {}
    item = ComputeQuotaBase(**d)
    assert item.per_user == d.get("per_user", False)
    assert item.type == QuotaType.COMPUTE.value
    assert item.cores == d.get("cores")
    assert item.instances == d.get("instances")
    assert item.ram == d.get("ram")


@parametrize_with_cases("key, value", cases=CaseInvalidAttr)
def test_invalid_base(key: str, value: Any) -> None:
    d = {key: value}
    with pytest.raises(ValueError):
        ComputeQuotaBase(**d)


def test_create() -> None:
    assert issubclass(ComputeQuotaCreate, BaseNodeCreate)
    assert issubclass(ComputeQuotaCreate, ComputeQuotaBase)


@parametrize_with_cases(
    "key, value", cases=[CaseInvalidAttr, CaseAttr], has_tag=["update"]
)
def test_update(key: str, value: Any) -> None:
    assert issubclass(ComputeQuotaUpdate, BaseNodeCreate)
    assert issubclass(ComputeQuotaUpdate, ComputeQuotaBase)
    d = {key: value} if key else {}
    item = ComputeQuotaUpdate(**d)
    assert item.type == QuotaType.COMPUTE.value


def test_query() -> None:
    assert issubclass(ComputeQuotaQuery, BaseNodeQuery)


# TODO Test all read classes
