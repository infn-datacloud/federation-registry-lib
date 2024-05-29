from typing import Any

from pytest_cases import parametrize_with_cases

from fed_reg.provider.enum import ProviderStatus, ProviderType
from fed_reg.provider.models import Provider
from fed_reg.provider.schemas import (
    ProviderBase,
    ProviderBasePublic,
    ProviderRead,
    ProviderReadPublic,
    ProviderUpdate,
)
from tests.create_dict import provider_schema_dict


@parametrize_with_cases("key, value", has_tag="base_public")
def test_base_public(key: str, value: str) -> None:
    d = provider_schema_dict()
    if key:
        d[key] = value
    item = ProviderBasePublic(**d)
    assert item.description == d.get("description", "")
    assert item.name == d.get("name")
    assert item.type == d.get("type").value


@parametrize_with_cases("key, value", has_tag="base")
def test_base(key: str, value: Any) -> None:
    d = provider_schema_dict()
    if key:
        d[key] = value
    item = ProviderBase(**d)
    assert item.name == d.get("name")
    assert item.type == d.get("type").value
    assert item.status == d.get("status", ProviderStatus.ACTIVE).value
    assert item.is_public == d.get("is_public", False)
    assert item.support_emails == d.get("support_emails", [])


@parametrize_with_cases("key, value", has_tag="base_public")
def test_read_public(provider_model: Provider, key: str, value: str) -> None:
    if key:
        if isinstance(value, ProviderType):
            value = value.value
        provider_model.__setattr__(key, value)
    item = ProviderReadPublic.from_orm(provider_model)

    assert item.uid
    assert item.uid == provider_model.uid
    assert item.description == provider_model.description
    assert item.name == provider_model.name
    assert item.type == provider_model.type


@parametrize_with_cases("key, value", has_tag="base")
def test_read(provider_model: Provider, key: str, value: Any) -> None:
    if key:
        if isinstance(value, (ProviderType, ProviderStatus)):
            value = value.value
        provider_model.__setattr__(key, value)
    item = ProviderRead.from_orm(provider_model)

    assert item.uid
    assert item.uid == provider_model.uid
    assert item.description == provider_model.description
    assert item.name == provider_model.name
    assert item.type == provider_model.type
    if provider_model.status:
        assert item.status == provider_model.status
    else:
        assert item.status == ProviderStatus.ACTIVE.value
    assert item.is_public == provider_model.is_public
    assert item.support_emails == provider_model.support_emails


@parametrize_with_cases("key, value", has_tag="update")
def test_update(key: str, value: Any) -> None:
    d = provider_schema_dict()
    if key:
        d[key] = value
    item = ProviderUpdate(**d)
    assert item.name == d.get("name")
    assert item.type == (d.get("type").value if d.get("type") else None)
