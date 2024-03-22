from typing import Any, Tuple

import pytest
from neomodel import CardinalityViolation, RelationshipManager, RequiredProperty
from pytest_cases import parametrize, parametrize_with_cases

from fed_reg.auth_method.models import AuthMethod
from fed_reg.identity_provider.models import IdentityProvider
from fed_reg.provider.models import Provider
from fed_reg.user_group.models import UserGroup
from tests.create_dict import auth_method_dict, identity_provider_model_dict
from tests.utils import random_lower_string


class CaseMissing:
    @parametrize(value=["endpoint", "group_claim"])
    def case_missing(self, value: str) -> str:
        return value


class CaseAttr:
    @parametrize(key=["description"])
    def case_str(self, key: str) -> Tuple[str, str]:
        return key, random_lower_string()


def test_default_attr() -> None:
    d = identity_provider_model_dict()
    item = IdentityProvider(**d)
    assert item.uid is not None
    assert item.description == ""
    assert item.endpoint == d.get("endpoint")
    assert item.group_claim == d.get("group_claim")
    assert isinstance(item.providers, RelationshipManager)
    assert isinstance(item.user_groups, RelationshipManager)


@parametrize_with_cases("missing_attr", cases=CaseMissing)
def test_missing_attr(missing_attr: str) -> None:
    d = identity_provider_model_dict()
    d[missing_attr] = None
    item = IdentityProvider(**d)
    with pytest.raises(RequiredProperty):
        item.save()


@parametrize_with_cases("key, value", cases=CaseAttr)
def test_attr(key: str, value: Any) -> None:
    d = identity_provider_model_dict()
    d[key] = value

    item = IdentityProvider(**d)
    saved = item.save()

    assert saved.element_id_property is not None
    assert saved.uid == item.uid
    assert saved.__getattribute__(key) == value


def test_required_rel(identity_provider_model: IdentityProvider) -> None:
    with pytest.raises(CardinalityViolation):
        identity_provider_model.providers.all()
    with pytest.raises(CardinalityViolation):
        identity_provider_model.providers.single()


def test_optional_rel(identity_provider_model: IdentityProvider) -> None:
    assert len(identity_provider_model.user_groups.all()) == 0
    assert identity_provider_model.user_groups.single() is None


def test_linked_user_group(
    identity_provider_model: IdentityProvider, user_group_model: UserGroup
) -> None:
    assert identity_provider_model.user_groups.name
    assert identity_provider_model.user_groups.source
    assert isinstance(identity_provider_model.user_groups.source, IdentityProvider)
    assert identity_provider_model.user_groups.source.uid == identity_provider_model.uid
    assert identity_provider_model.user_groups.definition
    assert identity_provider_model.user_groups.definition["node_class"] == UserGroup

    r = identity_provider_model.user_groups.connect(user_group_model)
    assert r is True

    assert len(identity_provider_model.user_groups.all()) == 1
    user_group = identity_provider_model.user_groups.single()
    assert isinstance(user_group, UserGroup)
    assert user_group.uid == user_group_model.uid


def test_multiple_linked_user_groups(
    identity_provider_model: IdentityProvider, user_group_model: UserGroup
) -> None:
    identity_provider_model.user_groups.connect(user_group_model)
    identity_provider_model.user_groups.connect(user_group_model)
    assert len(identity_provider_model.user_groups.all()) == 2


def test_linked_provider(
    identity_provider_model: IdentityProvider, provider_model: Provider
) -> None:
    assert identity_provider_model.providers.name
    assert identity_provider_model.providers.source
    assert isinstance(identity_provider_model.providers.source, IdentityProvider)
    assert identity_provider_model.providers.source.uid == identity_provider_model.uid
    assert identity_provider_model.providers.definition
    assert identity_provider_model.providers.definition["node_class"] == Provider

    d = auth_method_dict()
    r = identity_provider_model.providers.connect(provider_model, d)
    assert isinstance(r, AuthMethod)
    assert r.idp_name == d["idp_name"]
    assert r.protocol == d["protocol"]

    assert len(identity_provider_model.providers.all()) == 1
    provider = identity_provider_model.providers.single()
    assert isinstance(provider, Provider)
    assert provider.uid == provider_model.uid


def test_multiple_linked_providers(
    identity_provider_model: IdentityProvider, provider_model: Provider
) -> None:
    identity_provider_model.providers.connect(provider_model, auth_method_dict())
    identity_provider_model.providers.connect(provider_model, auth_method_dict())
    assert len(identity_provider_model.providers.all()) == 2
