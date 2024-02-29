from random import randint
from typing import Any, Literal, Tuple
from uuid import uuid4

import pytest
from pytest_cases import case, parametrize, parametrize_with_cases

from fed_reg.models import BaseNodeCreate, BaseNodeQuery, BaseNodeRead
from fed_reg.provider.schemas_extended import BlockStorageQuotaCreateExtended
from fed_reg.quota.enum import QuotaType
from fed_reg.quota.models import BlockStorageQuota
from fed_reg.quota.schemas import (
    BlockStorageQuotaBase,
    BlockStorageQuotaCreate,
    BlockStorageQuotaQuery,
    BlockStorageQuotaRead,
    BlockStorageQuotaReadPublic,
    BlockStorageQuotaUpdate,
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

    @parametrize(value=[-1, randint(0, 100)])
    @parametrize(attr=["gigabytes", "per_volume_gigabytes", "volumes"])
    def case_integer(self, attr: str, value: int) -> Tuple[str, int]:
        return attr, value


class CaseInvalidAttr:
    @parametrize(attr=["gigabytes", "per_volume_gigabytes", "volumes"])
    def case_integer(self, attr: str) -> Tuple[str, int]:
        return attr, randint(-100, -2)

    @parametrize(value=[i for i in QuotaType if i != QuotaType.BLOCK_STORAGE])
    def case_type(self, value: QuotaType) -> Tuple[Literal["type"], QuotaType]:
        return "type", value


@parametrize_with_cases("key, value", cases=CaseAttr)
def test_base(key: str, value: Any) -> None:
    assert issubclass(BlockStorageQuotaBase, QuotaBase)
    d = {key: value} if key else {}
    item = BlockStorageQuotaBase(**d)
    assert item.per_user == d.get("per_user", False)
    assert item.type == QuotaType.BLOCK_STORAGE.value
    assert item.gigabytes == d.get("gigabytes")
    assert item.per_volume_gigabytes == d.get("per_volume_gigabytes")
    assert item.volumes == d.get("volumes")


@parametrize_with_cases("key, value", cases=CaseInvalidAttr)
def test_invalid_base(key: str, value: Any) -> None:
    d = {key: value}
    with pytest.raises(ValueError):
        BlockStorageQuotaBase(**d)


def test_create() -> None:
    assert issubclass(BlockStorageQuotaCreate, BaseNodeCreate)
    assert issubclass(BlockStorageQuotaCreate, BlockStorageQuotaBase)


@parametrize_with_cases(
    "key, value", cases=[CaseInvalidAttr, CaseAttr], has_tag=["update"]
)
def test_update(key: str, value: Any) -> None:
    assert issubclass(BlockStorageQuotaUpdate, BaseNodeCreate)
    assert issubclass(BlockStorageQuotaUpdate, BlockStorageQuotaBase)
    d = {key: value} if key else {}
    item = BlockStorageQuotaUpdate(**d)
    assert item.type == QuotaType.BLOCK_STORAGE.value


def test_query() -> None:
    assert issubclass(BlockStorageQuotaQuery, BaseNodeQuery)


def test_create_extended() -> None:
    assert issubclass(BlockStorageQuotaCreateExtended, BlockStorageQuotaCreate)
    d = {"project": uuid4()}
    item = BlockStorageQuotaCreateExtended(**d)
    assert item.project == d["project"].hex


def test_invalid_create_extended() -> None:
    d = {}
    with pytest.raises(ValueError):
        BlockStorageQuotaCreateExtended(**d)


@parametrize_with_cases("key, value", cases=CaseAttr, has_tag=["base_public"])
def test_read_public(
    block_storage_quota_model: BlockStorageQuota, key: str, value: str
) -> None:
    assert issubclass(BlockStorageQuotaReadPublic, QuotaBase)
    assert issubclass(BlockStorageQuotaReadPublic, BaseNodeRead)
    assert BlockStorageQuotaReadPublic.__config__.orm_mode

    if key:
        block_storage_quota_model.__setattr__(key, value)
    item = BlockStorageQuotaReadPublic.from_orm(block_storage_quota_model)

    assert item.uid
    assert item.uid == block_storage_quota_model.uid
    assert item.description == block_storage_quota_model.description
    assert item.per_user == block_storage_quota_model.per_user


@parametrize_with_cases("key, value", cases=CaseAttr)
def test_read(
    block_storage_quota_model: BlockStorageQuota, key: str, value: Any
) -> None:
    assert issubclass(BlockStorageQuotaRead, BlockStorageQuotaBase)
    assert issubclass(BlockStorageQuotaRead, BaseNodeRead)
    assert BlockStorageQuotaRead.__config__.orm_mode

    if key:
        block_storage_quota_model.__setattr__(key, value)
    print(block_storage_quota_model)
    item = BlockStorageQuotaRead.from_orm(block_storage_quota_model)

    assert item.uid
    assert item.uid == block_storage_quota_model.uid
    assert item.description == block_storage_quota_model.description
    assert item.per_user == block_storage_quota_model.per_user
    assert item.type == block_storage_quota_model.type
    assert item.gigabytes == block_storage_quota_model.gigabytes
    assert item.per_volume_gigabytes == block_storage_quota_model.per_volume_gigabytes
    assert item.volumes == block_storage_quota_model.volumes


@parametrize_with_cases("key, value", cases=CaseInvalidAttr)
def test_invalid_read(
    block_storage_quota_model: BlockStorageQuota, key: str, value: str
) -> None:
    block_storage_quota_model.__setattr__(key, value)
    with pytest.raises(ValueError):
        BlockStorageQuotaRead.from_orm(block_storage_quota_model)


# TODO Test read extended classes
