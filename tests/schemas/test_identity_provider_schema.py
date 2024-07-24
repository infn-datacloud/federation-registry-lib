from typing import Any

from pytest_cases import parametrize_with_cases

from fed_reg.auth_method.schemas import AuthMethodCreate
from fed_reg.identity_provider.models import IdentityProvider
from fed_reg.identity_provider.schemas import (
    IdentityProviderBase,
    IdentityProviderBasePublic,
    IdentityProviderRead,
    IdentityProviderReadPublic,
    IdentityProviderUpdate,
)
from fed_reg.provider.schemas_extended import (
    IdentityProviderCreateExtended,
    UserGroupCreateExtended,
)
from tests.create_dict import auth_method_dict, identity_provider_schema_dict


@parametrize_with_cases("key, value", has_tag="base_public")
def test_base_public(key: str, value: str) -> None:
    d = identity_provider_schema_dict()
    if key:
        d[key] = value
    item = IdentityProviderBasePublic(**d)
    assert item.description == d.get("description", "")
    assert item.endpoint == d.get("endpoint")


@parametrize_with_cases("key, value", has_tag="base")
def test_base(key: str, value: Any) -> None:
    d = identity_provider_schema_dict()
    if key:
        d[key] = value
    item = IdentityProviderBase(**d)
    assert item.endpoint == d.get("endpoint")
    assert item.group_claim == d.get("group_claim")


@parametrize_with_cases("key, value", has_tag="update")
def test_update(key: str, value: Any) -> None:
    d = identity_provider_schema_dict()
    if key:
        d[key] = value
    item = IdentityProviderUpdate(**d)
    assert item.endpoint == d.get("endpoint")
    assert item.group_claim == d.get("group_claim")


@parametrize_with_cases("user_groups", has_tag="create_extended")
def test_create_extended(user_groups: list[UserGroupCreateExtended]) -> None:
    d = identity_provider_schema_dict()
    d["relationship"] = AuthMethodCreate(**auth_method_dict())
    d["user_groups"] = user_groups
    item = IdentityProviderCreateExtended(**d)
    assert item.relationship == d["relationship"]
    assert item.user_groups == d["user_groups"]


@parametrize_with_cases("key, value", has_tag="base_public")
def test_read_public(
    identity_provider_model: IdentityProvider, key: str, value: str
) -> None:
    if key:
        identity_provider_model.__setattr__(key, value)
    item = IdentityProviderReadPublic.from_orm(identity_provider_model)

    assert item.uid
    assert item.uid == identity_provider_model.uid
    assert item.description == identity_provider_model.description
    assert item.endpoint == identity_provider_model.endpoint


@parametrize_with_cases("key, value", has_tag="base")
def test_read(identity_provider_model: IdentityProvider, key: str, value: Any) -> None:
    if key:
        identity_provider_model.__setattr__(key, value)
    item = IdentityProviderRead.from_orm(identity_provider_model)

    assert item.uid
    assert item.uid == identity_provider_model.uid
    assert item.description == identity_provider_model.description
    assert item.endpoint == identity_provider_model.endpoint
    assert item.group_claim == identity_provider_model.group_claim


# TODO Test read extended classes
