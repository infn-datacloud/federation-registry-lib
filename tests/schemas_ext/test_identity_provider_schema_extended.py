import pytest
from pydantic import ValidationError
from pytest_cases import parametrize_with_cases

from fedreg.auth_method.schemas import AuthMethodRead
from fedreg.core import BaseReadPrivateExtended, BaseReadPublicExtended
from fedreg.identity_provider.models import IdentityProvider
from fedreg.identity_provider.schemas import (
    IdentityProviderRead,
    IdentityProviderReadPublic,
)
from fedreg.identity_provider.schemas_extended import (
    IdentityProviderReadExtended,
    IdentityProviderReadExtendedPublic,
    ProviderReadExtended,
    ProviderReadExtendedPublic,
)
from fedreg.provider.models import Provider
from fedreg.provider.schemas import ProviderRead, ProviderReadPublic
from fedreg.user_group.models import UserGroup
from tests.models.utils import auth_method_model_dict


def test_class_inheritance():
    assert issubclass(IdentityProviderReadExtended, BaseReadPrivateExtended)
    assert issubclass(IdentityProviderReadExtended, IdentityProviderRead)
    assert (
        IdentityProviderReadExtended.__fields__["schema_type"].default
        == "private_extended"
    )
    assert IdentityProviderReadExtended.__config__.orm_mode is True

    assert issubclass(IdentityProviderReadExtendedPublic, BaseReadPublicExtended)
    assert issubclass(IdentityProviderReadExtendedPublic, IdentityProviderReadPublic)
    assert (
        IdentityProviderReadExtendedPublic.__fields__["schema_type"].default
        == "public_extended"
    )
    assert IdentityProviderReadExtendedPublic.__config__.orm_mode is True

    assert issubclass(ProviderReadExtended, ProviderRead)
    assert issubclass(ProviderReadExtendedPublic, ProviderReadPublic)


@parametrize_with_cases("providers", has_tag="providers")
def test_read_ext_with_providers(
    identity_provider_model: IdentityProvider, providers: list[Provider]
) -> None:
    for provider in providers:
        identity_provider_model.providers.connect(provider, auth_method_model_dict())

    item = IdentityProviderReadExtendedPublic.from_orm(identity_provider_model)
    assert len(item.user_groups) == 0
    assert len(item.providers) == len(providers)

    item = IdentityProviderReadExtended.from_orm(identity_provider_model)
    assert len(item.user_groups) == 0
    assert len(item.providers) == len(providers)


@parametrize_with_cases("user_groups", has_tag="user_groups")
def test_read_ext_with_user_groups(
    identity_provider_model: IdentityProvider,
    provider_model: Provider,
    user_groups: list[UserGroup],
) -> None:
    auth_method = auth_method_model_dict()
    identity_provider_model.providers.connect(provider_model, auth_method)
    for user_group in user_groups:
        identity_provider_model.user_groups.connect(user_group)

    item = IdentityProviderReadExtendedPublic.from_orm(identity_provider_model)
    assert len(item.user_groups) == len(user_groups)
    assert len(item.providers) == 1
    assert isinstance(item.providers[0], ProviderReadExtendedPublic)
    assert item.providers[0].relationship == AuthMethodRead(**auth_method)

    item = IdentityProviderReadExtended.from_orm(identity_provider_model)
    assert len(item.user_groups) == len(user_groups)
    assert len(item.providers) == 1
    assert isinstance(item.providers[0], ProviderReadExtended)
    assert item.providers[0].relationship == AuthMethodRead(**auth_method)


def test_provider_read_ext(
    identity_provider_model: IdentityProvider, provider_model: Provider
):
    with pytest.raises(ValidationError):
        ProviderReadExtended.from_orm(provider_model)
    auth_method = auth_method_model_dict()
    identity_provider_model.providers.connect(provider_model, auth_method)
    identity_provider = IdentityProviderReadExtended.from_orm(identity_provider_model)
    assert len(identity_provider.providers) == 1
    assert isinstance(identity_provider.providers[0], ProviderReadExtended)
    assert identity_provider.providers[0].relationship == AuthMethodRead(**auth_method)


def test_provider_read_ext_public(
    identity_provider_model: IdentityProvider, provider_model: Provider
):
    with pytest.raises(ValidationError):
        ProviderReadExtendedPublic.from_orm(provider_model)
    auth_method = auth_method_model_dict()
    identity_provider_model.providers.connect(provider_model, auth_method)
    identity_provider = IdentityProviderReadExtendedPublic.from_orm(
        identity_provider_model
    )
    assert len(identity_provider.providers) == 1
    assert isinstance(identity_provider.providers[0], ProviderReadExtendedPublic)
    assert identity_provider.providers[0].relationship == AuthMethodRead(**auth_method)
