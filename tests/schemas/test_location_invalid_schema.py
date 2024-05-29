from typing import Any

import pytest
from pytest_cases import parametrize_with_cases

from fed_reg.location.models import Location
from fed_reg.location.schemas import (
    LocationBase,
    LocationBasePublic,
    LocationRead,
    LocationReadPublic,
)
from tests.create_dict import location_schema_dict


@parametrize_with_cases("key, value", has_tag="base_public")
def test_invalid_base_public(key: str, value: None) -> None:
    d = location_schema_dict()
    d[key] = value
    with pytest.raises(ValueError):
        LocationBasePublic(**d)


@parametrize_with_cases("key, value")
def test_invalid_base(key: str, value: Any) -> None:
    d = location_schema_dict()
    d[key] = value
    with pytest.raises(ValueError):
        LocationBase(**d)


@parametrize_with_cases("key, value", has_tag="base_public")
def test_invalid_read_public(location_model: Location, key: str, value: str) -> None:
    location_model.__setattr__(key, value)
    with pytest.raises(ValueError):
        LocationReadPublic.from_orm(location_model)


@parametrize_with_cases("key, value")
def test_invalid_read(location_model: Location, key: str, value: str) -> None:
    location_model.__setattr__(key, value)
    with pytest.raises(ValueError):
        LocationRead.from_orm(location_model)
