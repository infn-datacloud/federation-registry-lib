from typing import Any, Optional

import pytest
from pytest_cases import parametrize_with_cases

from fed_reg.auth_method.schemas import AuthMethodCreate
from fed_reg.identity_provider.models import IdentityProvider
from fed_reg.identity_provider.schemas import (
    IdentityProviderBase,
    IdentityProviderBasePublic,
    IdentityProviderRead,
    IdentityProviderReadPublic,
)
from fed_reg.provider.schemas_extended import (
    IdentityProviderCreateExtended,
    UserGroupCreateExtended,
)
from tests.create_dict import auth_method_dict, identity_provider_schema_dict


@parametrize_with_cases("key, value", has_tag="base_public")
def test_invalid_base_public(key: str, value: None) -> None:
    d = identity_provider_schema_dict()
    d[key] = value
    with pytest.raises(ValueError):
        IdentityProviderBasePublic(**d)


@parametrize_with_cases("key, value", has_tag="base")
def test_invalid_base(key: str, value: Any) -> None:
    d = identity_provider_schema_dict()
    d[key] = value
    with pytest.raises(ValueError):
        IdentityProviderBase(**d)


@parametrize_with_cases("key, value", has_tag="base_public")
def test_invalid_read_public(
    identity_provider_model: IdentityProvider, key: str, value: str
) -> None:
    identity_provider_model.__setattr__(key, value)
    with pytest.raises(ValueError):
        IdentityProviderReadPublic.from_orm(identity_provider_model)


@parametrize_with_cases("key, value", has_tag="base")
def test_invalid_read(
    identity_provider_model: IdentityProvider, key: str, value: str
) -> None:
    identity_provider_model.__setattr__(key, value)
    with pytest.raises(ValueError):
        IdentityProviderRead.from_orm(identity_provider_model)


@parametrize_with_cases("attr, value, msg", has_tag="create_extended")
def test_invalid_create_extended(
    user_group_create_ext_schema: UserGroupCreateExtended,
    attr: str,
    value: UserGroupCreateExtended,
    msg: Optional[str],
) -> None:
    d = identity_provider_schema_dict()
    d["relationship"] = (
        value if attr == "relationship" else AuthMethodCreate(**auth_method_dict())
    )
    d["user_groups"] = value if attr == "user_groups" else user_group_create_ext_schema
    with pytest.raises(ValueError, match=msg):
        IdentityProviderCreateExtended(**d)
