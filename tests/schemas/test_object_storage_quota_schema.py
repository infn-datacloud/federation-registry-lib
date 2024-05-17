# from random import randint
from typing import Any, Literal
from uuid import uuid4

import pytest
from pytest_cases import case, parametrize, parametrize_with_cases

from fed_reg.models import BaseNodeCreate, BaseNodeQuery, BaseNodeRead
from fed_reg.provider.schemas_extended import ObjectStorageQuotaCreateExtended
from fed_reg.quota.enum import QuotaType
from fed_reg.quota.models import ObjectStorageQuota
from fed_reg.quota.schemas import (
    ObjectStorageQuotaBase,
    ObjectStorageQuotaCreate,
    ObjectStorageQuotaQuery,
    ObjectStorageQuotaRead,
    ObjectStorageQuotaReadPublic,
    ObjectStorageQuotaUpdate,
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

    # TODO: set correct attributes
    # @parametrize(value=[-1, randint(0, 100)])
    # @parametrize(attr=["gigabytes", "per_volume_gigabytes", "volumes"])
    # def case_integer(self, attr: str, value: int) -> tuple[str, int]:
    #     return attr, value


class CaseInvalidAttr:
    # TODO: set correct attributes
    # @parametrize(attr=["gigabytes", "per_volume_gigabytes", "volumes"])
    # def case_integer(self, attr: str) -> tuple[str, int]:
    #    return attr, randint(-100, -2)

    @parametrize(value=[i for i in QuotaType if i != QuotaType.OBJECT_STORAGE])
    def case_type(self, value: QuotaType) -> tuple[Literal["type"], QuotaType]:
        return "type", value


@parametrize_with_cases("key, value", cases=CaseAttr)
def test_base(key: str, value: Any) -> None:
    assert issubclass(ObjectStorageQuotaBase, QuotaBase)
    d = {key: value} if key else {}
    item = ObjectStorageQuotaBase(**d)
    assert item.per_user == d.get("per_user", False)
    assert item.type == QuotaType.OBJECT_STORAGE.value
    # TODO: understand attributes


@parametrize_with_cases("key, value", cases=CaseInvalidAttr)
def test_invalid_base(key: str, value: Any) -> None:
    d = {key: value}
    with pytest.raises(ValueError):
        ObjectStorageQuotaBase(**d)


def test_create() -> None:
    assert issubclass(ObjectStorageQuotaCreate, BaseNodeCreate)
    assert issubclass(ObjectStorageQuotaCreate, ObjectStorageQuotaBase)


@parametrize_with_cases(
    "key, value", cases=[CaseInvalidAttr, CaseAttr], has_tag=["update"]
)
def test_update(key: str, value: Any) -> None:
    assert issubclass(ObjectStorageQuotaUpdate, BaseNodeCreate)
    assert issubclass(ObjectStorageQuotaUpdate, ObjectStorageQuotaBase)
    d = {key: value} if key else {}
    item = ObjectStorageQuotaUpdate(**d)
    assert item.type == QuotaType.OBJECT_STORAGE.value


def test_query() -> None:
    assert issubclass(ObjectStorageQuotaQuery, BaseNodeQuery)


def test_create_extended() -> None:
    assert issubclass(ObjectStorageQuotaCreateExtended, ObjectStorageQuotaCreate)
    d = {"project": uuid4()}
    item = ObjectStorageQuotaCreateExtended(**d)
    assert item.project == d["project"].hex


def test_invalid_create_extended() -> None:
    d = {}
    with pytest.raises(ValueError):
        ObjectStorageQuotaCreateExtended(**d)


@parametrize_with_cases("key, value", cases=CaseAttr, has_tag=["base_public"])
def test_read_public(
    object_storage_quota_model: ObjectStorageQuota, key: str, value: str
) -> None:
    assert issubclass(ObjectStorageQuotaReadPublic, QuotaBase)
    assert issubclass(ObjectStorageQuotaReadPublic, BaseNodeRead)
    assert ObjectStorageQuotaReadPublic.__config__.orm_mode

    if key:
        object_storage_quota_model.__setattr__(key, value)
    item = ObjectStorageQuotaReadPublic.from_orm(object_storage_quota_model)

    assert item.uid
    assert item.uid == object_storage_quota_model.uid
    assert item.description == object_storage_quota_model.description
    assert item.per_user == object_storage_quota_model.per_user


@parametrize_with_cases("key, value", cases=CaseAttr)
def test_read(
    object_storage_quota_model: ObjectStorageQuota, key: str, value: Any
) -> None:
    assert issubclass(ObjectStorageQuotaRead, ObjectStorageQuotaBase)
    assert issubclass(ObjectStorageQuotaRead, BaseNodeRead)
    assert ObjectStorageQuotaRead.__config__.orm_mode

    if key:
        object_storage_quota_model.__setattr__(key, value)
    item = ObjectStorageQuotaRead.from_orm(object_storage_quota_model)

    assert item.uid
    assert item.uid == object_storage_quota_model.uid
    assert item.description == object_storage_quota_model.description
    assert item.per_user == object_storage_quota_model.per_user
    assert item.type == object_storage_quota_model.type
    # TODO: Understand attributes


@parametrize_with_cases("key, value", cases=CaseInvalidAttr)
def test_invalid_read(
    object_storage_quota_model: ObjectStorageQuota, key: str, value: str
) -> None:
    object_storage_quota_model.__setattr__(key, value)
    with pytest.raises(ValueError):
        ObjectStorageQuotaRead.from_orm(object_storage_quota_model)


# TODO Test read extended classes
