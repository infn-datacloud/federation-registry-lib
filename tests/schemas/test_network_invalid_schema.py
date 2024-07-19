from typing import Any, Optional
from uuid import UUID

import pytest
from pytest_cases import parametrize_with_cases

from fed_reg.network.models import Network
from fed_reg.network.schemas import (
    NetworkBase,
    NetworkBasePublic,
    NetworkRead,
    NetworkReadPublic,
)
from fed_reg.provider.schemas_extended import NetworkCreateExtended
from tests.create_dict import network_schema_dict


@parametrize_with_cases("key, value", has_tag="base_public")
def test_invalid_base_public(key: str, value: None) -> None:
    d = network_schema_dict()
    d[key] = value
    with pytest.raises(ValueError):
        NetworkBasePublic(**d)


@parametrize_with_cases("key, value", has_tag="base")
def test_invalid_base(key: str, value: Any) -> None:
    d = network_schema_dict()
    d[key] = value
    with pytest.raises(ValueError):
        NetworkBase(**d)


@parametrize_with_cases("key, value", has_tag="base_public")
def test_invalid_read_public(network_model: Network, key: str, value: str) -> None:
    network_model.__setattr__(key, value)
    with pytest.raises(ValueError):
        NetworkReadPublic.from_orm(network_model)


@parametrize_with_cases("key, value", has_tag="base")
def test_invalid_read(network_model: Network, key: str, value: str) -> None:
    network_model.__setattr__(key, value)
    with pytest.raises(ValueError):
        NetworkRead.from_orm(network_model)


@parametrize_with_cases("project, msg", has_tag="create_extended")
def test_invalid_create_extended(project: Optional[UUID], msg: str) -> None:
    d = network_schema_dict()
    d["is_shared"] = project is not None
    d["project"] = project
    with pytest.raises(ValueError, match=msg):
        NetworkCreateExtended(**d)
