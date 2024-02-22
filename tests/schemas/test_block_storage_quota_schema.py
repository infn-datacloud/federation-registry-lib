from random import randint
from typing import Any, Literal, Tuple

import pytest
from pytest_cases import case, parametrize, parametrize_with_cases

from fed_reg.models import BaseNodeCreate, BaseNodeQuery
from fed_reg.quota.enum import QuotaType
from fed_reg.quota.schemas import (
    BlockStorageQuotaBase,
    BlockStorageQuotaCreate,
    BlockStorageQuotaQuery,
    BlockStorageQuotaUpdate,
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


# TODO Test all read classes
