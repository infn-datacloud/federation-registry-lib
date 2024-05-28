from typing import Any

from pytest_cases import parametrize_with_cases

from fed_reg.provider.schemas_extended import SLACreateExtended, UserGroupCreateExtended
from fed_reg.user_group.models import UserGroup
from fed_reg.user_group.schemas import (
    UserGroupBase,
    UserGroupBasePublic,
    UserGroupRead,
    UserGroupReadPublic,
    UserGroupUpdate,
)
from tests.create_dict import user_group_schema_dict


@parametrize_with_cases("key, value", has_tag="base_public")
def test_base_public(key: str, value: str) -> None:
    d = user_group_schema_dict()
    if key:
        d[key] = value
    item = UserGroupBasePublic(**d)
    assert item.description == d.get("description", "")
    assert item.name == d.get("name")


@parametrize_with_cases("key, value", has_tag="base")
def test_base(key: str, value: Any) -> None:
    d = user_group_schema_dict()
    if key:
        d[key] = value
    item = UserGroupBase(**d)
    assert item.name == d.get("name")


@parametrize_with_cases("key, value", has_tag="update")
def test_update(key: str, value: Any) -> None:
    d = user_group_schema_dict()
    if key:
        d[key] = value
    item = UserGroupUpdate(**d)
    assert item.name == d.get("name")


def test_create_extended(sla_create_ext_schema: SLACreateExtended) -> None:
    d = user_group_schema_dict()
    d["sla"] = sla_create_ext_schema
    item = UserGroupCreateExtended(**d)
    assert item.sla == d["sla"]


@parametrize_with_cases("key, value", has_tag="base_public")
def test_read_public(user_group_model: UserGroup, key: str, value: str) -> None:
    if key:
        user_group_model.__setattr__(key, value)
    item = UserGroupReadPublic.from_orm(user_group_model)

    assert item.uid
    assert item.uid == user_group_model.uid
    assert item.description == user_group_model.description
    assert item.name == user_group_model.name


@parametrize_with_cases("key, value", has_tag="base")
def test_read(user_group_model: UserGroup, key: str, value: Any) -> None:
    if key:
        user_group_model.__setattr__(key, value)
    item = UserGroupRead.from_orm(user_group_model)

    assert item.uid
    assert item.uid == user_group_model.uid
    assert item.description == user_group_model.description
    assert item.name == user_group_model.name


# TODO Test read extended classes
