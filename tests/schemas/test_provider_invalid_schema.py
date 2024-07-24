from typing import Any

import pytest
from pytest_cases import parametrize_with_cases

from fed_reg.provider.models import Provider
from fed_reg.provider.schemas import (
    ProviderBase,
    ProviderBasePublic,
    ProviderRead,
    ProviderReadPublic,
)
from tests.create_dict import provider_schema_dict


@parametrize_with_cases("key, value", has_tag="base_public")
def test_invalid_base_public(key: str, value: Any) -> None:
    d = provider_schema_dict()
    d[key] = value
    with pytest.raises(ValueError):
        ProviderBasePublic(**d)


@parametrize_with_cases("key, value", has_tag="base")
def test_invalid_base(key: str, value: Any) -> None:
    d = provider_schema_dict()
    d[key] = value
    with pytest.raises(ValueError):
        ProviderBase(**d)


@parametrize_with_cases("key, value", has_tag="base_public")
def test_invalid_read_public(provider_model: Provider, key: str, value: str) -> None:
    provider_model.__setattr__(key, value)
    with pytest.raises(ValueError):
        ProviderReadPublic.from_orm(provider_model)


@parametrize_with_cases("key, value", has_tag="base")
def test_invalid_read(provider_model: Provider, key: str, value: str) -> None:
    provider_model.__setattr__(key, value)
    with pytest.raises(ValueError):
        ProviderRead.from_orm(provider_model)
