from typing import Any

import pytest
from pytest_cases import parametrize_with_cases

from fed_reg.provider.schemas_extended import (
    BlockStorageServiceCreateExtended,
    ComputeServiceCreateExtended,
    NetworkServiceCreateExtended,
    ObjectStorageServiceCreateExtended,
    RegionCreateExtended,
)
from fed_reg.region.models import Region
from fed_reg.region.schemas import (
    RegionBase,
    RegionBasePublic,
    RegionRead,
    RegionReadPublic,
)
from fed_reg.service.schemas import IdentityServiceCreate
from tests.create_dict import region_schema_dict


@parametrize_with_cases("key, value", has_tag="base_public")
def test_invalid_base_public(key: str, value: None) -> None:
    d = region_schema_dict()
    d[key] = value
    with pytest.raises(ValueError):
        RegionBasePublic(**d)


@parametrize_with_cases("key, value", has_tag="base")
def test_invalid_base(key: str, value: Any) -> None:
    d = region_schema_dict()
    d[key] = value
    with pytest.raises(ValueError):
        RegionBase(**d)


@parametrize_with_cases("key, value", has_tag="base_public")
def test_invalid_read_public(region_model: Region, key: str, value: str) -> None:
    region_model.__setattr__(key, value)
    with pytest.raises(ValueError):
        RegionReadPublic.from_orm(region_model)


@parametrize_with_cases("key, value", has_tag="base")
def test_invalid_read(region_model: Region, key: str, value: str) -> None:
    region_model.__setattr__(key, value)
    with pytest.raises(ValueError):
        RegionRead.from_orm(region_model)


@parametrize_with_cases("attr, values, msg", has_tag="create_extended")
def test_invalid_create_extended(
    attr: str,
    values: list[BlockStorageServiceCreateExtended]
    | list[ComputeServiceCreateExtended]
    | list[IdentityServiceCreate]
    | list[NetworkServiceCreateExtended]
    | list[ObjectStorageServiceCreateExtended],
    msg: str,
) -> None:
    d = region_schema_dict()
    d[attr] = values
    with pytest.raises(ValueError, match=msg):
        RegionCreateExtended(**d)
