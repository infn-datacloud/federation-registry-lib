from typing import Any, Literal

import pytest
from pytest_cases import case, parametrize_with_cases

from fed_reg.models import BaseNode, BaseNodeCreate, BaseNodeQuery, BaseNodeRead
from fed_reg.provider.schemas_extended import SLACreateExtended, UserGroupCreateExtended
from fed_reg.user_group.models import UserGroup
from fed_reg.user_group.schemas import (
    UserGroupBase,
    UserGroupBasePublic,
    UserGroupCreate,
    UserGroupQuery,
    UserGroupRead,
    UserGroupReadPublic,
    UserGroupUpdate,
)
from tests.create_dict import user_group_schema_dict
from tests.utils import random_lower_string


class CaseAttr:
    @case(tags=["base_public", "update"])
    def case_none(self) -> tuple[None, None]:
        return None, None

    @case(tags=["base_public"])
    def case_desc(self) -> tuple[Literal["description"], str]:
        return "description", random_lower_string()


class CaseInvalidAttr:
    @case(tags=["base_public", "update"])
    def case_attr(self) -> tuple[Literal["name"], None]:
        return "name", None


@parametrize_with_cases("key, value", cases=CaseAttr, has_tag=["base_public"])
def test_base_public(key: str, value: str) -> None:
    assert issubclass(UserGroupBasePublic, BaseNode)
    d = user_group_schema_dict()
    if key:
        d[key] = value
    item = UserGroupBasePublic(**d)
    assert item.description == d.get("description", "")
    assert item.name == d.get("name")


@parametrize_with_cases("key, value", cases=CaseInvalidAttr, has_tag=["base_public"])
def test_invalid_base_public(key: str, value: None) -> None:
    d = user_group_schema_dict()
    d[key] = value
    with pytest.raises(ValueError):
        UserGroupBasePublic(**d)


@parametrize_with_cases("key, value", cases=CaseAttr)
def test_base(key: str, value: Any) -> None:
    assert issubclass(UserGroupBase, UserGroupBasePublic)
    d = user_group_schema_dict()
    if key:
        d[key] = value
    item = UserGroupBase(**d)
    assert item.name == d.get("name")


@parametrize_with_cases("key, value", cases=CaseInvalidAttr)
def test_invalid_base(key: str, value: Any) -> None:
    d = user_group_schema_dict()
    d[key] = value
    with pytest.raises(ValueError):
        UserGroupBase(**d)


def test_create() -> None:
    assert issubclass(UserGroupCreate, BaseNodeCreate)
    assert issubclass(UserGroupCreate, UserGroupBase)


@parametrize_with_cases(
    "key, value", cases=[CaseInvalidAttr, CaseAttr], has_tag=["update"]
)
def test_update(key: str, value: Any) -> None:
    assert issubclass(UserGroupUpdate, BaseNodeCreate)
    assert issubclass(UserGroupUpdate, UserGroupBase)
    d = user_group_schema_dict()
    if key:
        d[key] = value
    item = UserGroupUpdate(**d)
    assert item.name == d.get("name")


def test_query() -> None:
    assert issubclass(UserGroupQuery, BaseNodeQuery)


def test_create_extended(sla_create_ext_schema: SLACreateExtended) -> None:
    assert issubclass(UserGroupCreateExtended, UserGroupCreate)
    d = user_group_schema_dict()
    d["sla"] = sla_create_ext_schema
    item = UserGroupCreateExtended(**d)
    assert item.sla == d["sla"]


def test_invalid_create_extended() -> None:
    d = user_group_schema_dict()
    with pytest.raises(ValueError):
        UserGroupCreateExtended(**d)


@parametrize_with_cases("key, value", cases=CaseAttr, has_tag=["base_public"])
def test_read_public(user_group_model: UserGroup, key: str, value: str) -> None:
    assert issubclass(UserGroupReadPublic, UserGroupBasePublic)
    assert issubclass(UserGroupReadPublic, BaseNodeRead)
    assert UserGroupReadPublic.__config__.orm_mode

    if key:
        user_group_model.__setattr__(key, value)
    item = UserGroupReadPublic.from_orm(user_group_model)

    assert item.uid
    assert item.uid == user_group_model.uid
    assert item.description == user_group_model.description
    assert item.name == user_group_model.name


@parametrize_with_cases("key, value", cases=CaseInvalidAttr, has_tag=["base_public"])
def test_invalid_read_public(user_group_model: UserGroup, key: str, value: str) -> None:
    user_group_model.__setattr__(key, value)
    with pytest.raises(ValueError):
        UserGroupReadPublic.from_orm(user_group_model)


@parametrize_with_cases("key, value", cases=CaseAttr)
def test_read(user_group_model: UserGroup, key: str, value: Any) -> None:
    assert issubclass(UserGroupRead, UserGroupBase)
    assert issubclass(UserGroupRead, BaseNodeRead)
    assert UserGroupRead.__config__.orm_mode

    if key:
        user_group_model.__setattr__(key, value)
    item = UserGroupRead.from_orm(user_group_model)

    assert item.uid
    assert item.uid == user_group_model.uid
    assert item.description == user_group_model.description
    assert item.name == user_group_model.name


@parametrize_with_cases("key, value", cases=CaseInvalidAttr)
def test_invalid_read(user_group_model: UserGroup, key: str, value: str) -> None:
    user_group_model.__setattr__(key, value)
    with pytest.raises(ValueError):
        UserGroupRead.from_orm(user_group_model)


# TODO Test read extended classes
