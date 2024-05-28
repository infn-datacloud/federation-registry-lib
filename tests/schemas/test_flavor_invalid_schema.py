from typing import Any
from uuid import UUID

import pytest
from pytest_cases import parametrize_with_cases

from fed_reg.flavor.models import Flavor
from fed_reg.flavor.schemas import (
    FlavorBase,
    FlavorBasePublic,
    FlavorRead,
    FlavorReadPublic,
)
from fed_reg.provider.schemas_extended import FlavorCreateExtended
from tests.create_dict import flavor_schema_dict


@parametrize_with_cases("key, value", has_tag="base_public")
def test_invalid_base_public(key: str, value: None) -> None:
    d = flavor_schema_dict()
    d[key] = value
    with pytest.raises(ValueError):
        FlavorBasePublic(**d)


@parametrize_with_cases("key, value", has_tag="base")
def test_invalid_base(key: str, value: Any) -> None:
    d = flavor_schema_dict()
    d[key] = value
    with pytest.raises(ValueError):
        FlavorBase(**d)


@parametrize_with_cases("key, value", has_tag="base_public")
def test_invalid_read_public(flavor_model: Flavor, key: str, value: str) -> None:
    flavor_model.__setattr__(key, value)
    with pytest.raises(ValueError):
        FlavorReadPublic.from_orm(flavor_model)


@parametrize_with_cases("key, value", has_tag="base")
def test_invalid_read(flavor_model: Flavor, key: str, value: str) -> None:
    flavor_model.__setattr__(key, value)
    with pytest.raises(ValueError):
        FlavorRead.from_orm(flavor_model)


@parametrize_with_cases("projects, msg", has_tag="create_extended")
def test_invalid_create_extended(projects: list[UUID], msg: str) -> None:
    d = flavor_schema_dict()
    if len(projects) == 0 or len(projects) == 2:
        d["is_public"] = False
    elif len(projects) == 1:
        d["is_public"] = True
    d["projects"] = projects
    with pytest.raises(ValueError, match=msg):
        FlavorCreateExtended(**d)
