from typing import Any

import pytest
from pytest_cases import parametrize_with_cases

from fed_reg.provider.schemas_extended import UserGroupCreateExtended
from fed_reg.user_group.models import UserGroup
from fed_reg.user_group.schemas import (
    UserGroupBase,
    UserGroupBasePublic,
    UserGroupRead,
    UserGroupReadPublic,
)
from tests.create_dict import user_group_schema_dict


@parametrize_with_cases("key, value")
def test_invalid_base_public(key: str, value: None) -> None:
    d = user_group_schema_dict()
    d[key] = value
    with pytest.raises(ValueError):
        UserGroupBasePublic(**d)


@parametrize_with_cases("key, value")
def test_invalid_base(key: str, value: Any) -> None:
    d = user_group_schema_dict()
    d[key] = value
    with pytest.raises(ValueError):
        UserGroupBase(**d)


@parametrize_with_cases("key, value")
def test_invalid_read_public(user_group_model: UserGroup, key: str, value: str) -> None:
    user_group_model.__setattr__(key, value)
    with pytest.raises(ValueError):
        UserGroupReadPublic.from_orm(user_group_model)


@parametrize_with_cases("key, value")
def test_invalid_read(user_group_model: UserGroup, key: str, value: str) -> None:
    user_group_model.__setattr__(key, value)
    with pytest.raises(ValueError):
        UserGroupRead.from_orm(user_group_model)


def test_invalid_create_extended() -> None:
    d = user_group_schema_dict()
    with pytest.raises(ValueError):
        UserGroupCreateExtended(**d)
