from random import randint
from typing import Any, Literal, Tuple
from uuid import uuid4

import pytest
from pytest_cases import case, parametrize, parametrize_with_cases

from fed_reg.models import BaseNodeCreate, BaseNodeQuery, BaseNodeRead
from fed_reg.provider.schemas_extended import ComputeQuotaCreateExtended
from fed_reg.quota.enum import QuotaType
from fed_reg.quota.models import ComputeQuota
from fed_reg.quota.schemas import (
    ComputeQuotaBase,
    ComputeQuotaCreate,
    ComputeQuotaQuery,
    ComputeQuotaRead,
    ComputeQuotaReadPublic,
    ComputeQuotaUpdate,
    QuotaBase,
)
from tests.utils import random_lower_string


class CaseAttr:
    @case(tags=["base_public", "update"])
    def case_none(self) -> Tuple[None, None]:
        return None, None

    @case(tags=["base_public"])
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


def test_create_extended() -> None:
    assert issubclass(ComputeQuotaCreateExtended, ComputeQuotaCreate)
    d = {"project": uuid4()}
    item = ComputeQuotaCreateExtended(**d)
    assert item.project == d["project"].hex


def test_invalid_create_extended() -> None:
    d = {}
    with pytest.raises(ValueError):
        ComputeQuotaCreateExtended(**d)


@parametrize_with_cases("key, value", cases=CaseAttr, has_tag=["base_public"])
def test_read_public(compute_quota_model: ComputeQuota, key: str, value: str) -> None:
    assert issubclass(ComputeQuotaReadPublic, QuotaBase)
    assert issubclass(ComputeQuotaReadPublic, BaseNodeRead)
    assert ComputeQuotaReadPublic.__config__.orm_mode

    if key:
        compute_quota_model.__setattr__(key, value)
    item = ComputeQuotaReadPublic.from_orm(compute_quota_model)

    assert item.uid
    assert item.uid == compute_quota_model.uid
    assert item.description == compute_quota_model.description
    assert item.per_user == compute_quota_model.per_user


@parametrize_with_cases("key, value", cases=CaseAttr)
def test_read(compute_quota_model: ComputeQuota, key: str, value: Any) -> None:
    assert issubclass(ComputeQuotaRead, ComputeQuotaBase)
    assert issubclass(ComputeQuotaRead, BaseNodeRead)
    assert ComputeQuotaRead.__config__.orm_mode

    if key:
        compute_quota_model.__setattr__(key, value)
    item = ComputeQuotaRead.from_orm(compute_quota_model)

    assert item.uid
    assert item.uid == compute_quota_model.uid
    assert item.description == compute_quota_model.description
    assert item.per_user == compute_quota_model.per_user
    assert item.type == compute_quota_model.type
    assert item.cores == compute_quota_model.cores
    assert item.instances == compute_quota_model.instances
    assert item.ram == compute_quota_model.ram


@parametrize_with_cases("key, value", cases=CaseInvalidAttr)
def test_invalid_read(compute_quota_model: ComputeQuota, key: str, value: str) -> None:
    compute_quota_model.__setattr__(key, value)
    with pytest.raises(ValueError):
        ComputeQuotaRead.from_orm(compute_quota_model)


# TODO Test read extended classes
