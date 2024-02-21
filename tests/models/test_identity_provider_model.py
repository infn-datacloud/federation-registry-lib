from typing import Any, Tuple
from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from neo4j.graph import Node, Relationship
from neomodel import CardinalityViolation, RelationshipManager, RequiredProperty
from pytest_cases import parametrize, parametrize_with_cases

from fed_reg.auth_method.models import AuthMethod
from fed_reg.identity_provider.models import IdentityProvider
from fed_reg.provider.models import Provider
from fed_reg.user_group.models import UserGroup
from tests.create_dict import auth_method_dict, identity_provider_dict
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
    d = identity_provider_dict()
    item = IdentityProvider(**d)
    assert item.uid is not None
    assert item.description == ""
    assert item.endpoint == d.get("endpoint")
    assert item.group_claim == d.get("group_claim")
    assert isinstance(item.providers, RelationshipManager)
    assert isinstance(item.user_groups, RelationshipManager)


@parametrize_with_cases("missing_attr", cases=CaseMissing)
def test_missing_attr(missing_attr: str) -> None:
    d = identity_provider_dict()
    d[missing_attr] = None
    item = IdentityProvider(**d)
    with pytest.raises(RequiredProperty):
        item.save()


@parametrize_with_cases("key, value", cases=CaseAttr)
def test_attr(db_core: MagicMock, key: str, value: Any) -> None:
    d = identity_provider_dict()
    d[key] = value

    element_id = f"{db_core.database_version}:{uuid4().hex}:0"
    db_core.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=0, properties=d)]],
        None,
    )

    item = IdentityProvider(**d)
    saved = item.save()

    assert saved.element_id_property == element_id
    assert saved.uid == item.uid
    assert saved.__getattribute__(key) == value


def test_required_rel(
    db_match: MagicMock, identity_provider_model: IdentityProvider
) -> None:
    db_match.cypher_query.return_value = ([], None)
    with pytest.raises(CardinalityViolation):
        identity_provider_model.providers.all()
    with pytest.raises(CardinalityViolation):
        identity_provider_model.providers.single()


def test_optional_rel(
    db_match: MagicMock, identity_provider_model: IdentityProvider
) -> None:
    db_match.cypher_query.return_value = ([], None)
    assert len(identity_provider_model.user_groups.all()) == 0
    assert identity_provider_model.user_groups.single() is None


def test_linked_user_group(
    db_rel_mgr: MagicMock,
    db_match: MagicMock,
    identity_provider_model: IdentityProvider,
    user_group_model: UserGroup,
) -> None:
    assert identity_provider_model.user_groups.name
    assert identity_provider_model.user_groups.source
    assert isinstance(identity_provider_model.user_groups.source, IdentityProvider)
    assert identity_provider_model.user_groups.source.uid == identity_provider_model.uid
    assert identity_provider_model.user_groups.definition
    assert identity_provider_model.user_groups.definition["node_class"] == UserGroup

    r = identity_provider_model.user_groups.connect(user_group_model)
    assert r is True

    db_match.cypher_query.return_value = ([[user_group_model]], ["user_groups_r1"])
    assert len(identity_provider_model.user_groups.all()) == 1
    user_group = identity_provider_model.user_groups.single()
    assert isinstance(user_group, UserGroup)
    assert user_group.uid == user_group_model.uid


def test_multiple_linked_user_groups(
    db_rel_mgr: MagicMock,
    db_match: MagicMock,
    identity_provider_model: IdentityProvider,
    user_group_model: UserGroup,
) -> None:
    db_match.cypher_query.return_value = (
        [[user_group_model], [user_group_model]],
        ["user_groups_r1", "user_groups_r2"],
    )
    assert len(identity_provider_model.user_groups.all()) == 2


def test_linked_providers(
    db_rel_mgr: MagicMock,
    db_match: MagicMock,
    db_core: MagicMock,
    identity_provider_model: IdentityProvider,
    provider_model: Provider,
) -> None:
    assert identity_provider_model.providers.name
    assert identity_provider_model.providers.source
    assert isinstance(identity_provider_model.providers.source, IdentityProvider)
    assert identity_provider_model.providers.source.uid == identity_provider_model.uid
    assert identity_provider_model.providers.definition
    assert identity_provider_model.providers.definition["node_class"] == Provider

    d = auth_method_dict()
    element_id = f"{db_core.database_version}:{uuid4().hex}:0"
    r = Relationship(..., element_id=element_id, id_=0, properties=d)
    r._start_node = Node(
        ...,
        element_id=identity_provider_model.element_id,
        id_=int(
            identity_provider_model.element_id[
                identity_provider_model.element_id.rfind(":") + 1 :
            ]
        ),
    )
    r._end_node = Node(
        ...,
        element_id=provider_model.element_id,
        id_=int(provider_model.element_id[provider_model.element_id.rfind(":") + 1 :]),
    )
    db_core.cypher_query.return_value = ([[r]], None)
    r = identity_provider_model.providers.connect(provider_model, d)
    assert isinstance(r, AuthMethod)
    assert r.idp_name == d["idp_name"]
    assert r.protocol == d["protocol"]

    db_match.cypher_query.return_value = ([[provider_model]], ["providers_r1"])
    assert len(identity_provider_model.providers.all()) == 1
    provider = identity_provider_model.providers.single()
    assert isinstance(provider, Provider)
    assert provider.uid == provider_model.uid


def test_multiple_linked_providers(
    db_rel_mgr: MagicMock,
    db_match: MagicMock,
    identity_provider_model: IdentityProvider,
    provider_model: Provider,
) -> None:
    db_match.cypher_query.return_value = (
        [[provider_model], [provider_model]],
        ["providers_r1", "providers_r2"],
    )
    assert len(identity_provider_model.providers.all()) == 2
