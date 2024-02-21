from typing import Any, Tuple
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest
from neo4j.graph import Node
from neomodel import (
    AttemptedCardinalityViolation,
    CardinalityViolation,
    RelationshipManager,
    RequiredProperty,
)
from pytest_cases import parametrize, parametrize_with_cases

from fed_reg.identity_provider.models import IdentityProvider
from fed_reg.sla.models import SLA
from fed_reg.user_group.models import UserGroup
from tests.create_dict import user_group_model_dict
from tests.utils import random_lower_string


class CaseAttr:
    @parametrize(key=["description"])
    def case_str(self, key: str) -> Tuple[str, str]:
        return key, random_lower_string()


def test_default_attr() -> None:
    d = user_group_model_dict()
    item = UserGroup(**d)
    assert item.uid is not None
    assert item.description == ""
    assert item.name == d.get("name")
    assert isinstance(item.identity_provider, RelationshipManager)
    assert isinstance(item.slas, RelationshipManager)


def test_missing_attr() -> None:
    item = UserGroup()
    with pytest.raises(RequiredProperty):
        item.save()


@parametrize_with_cases("key, value", cases=CaseAttr)
def test_attr(db_core: MagicMock, key: str, value: Any) -> None:
    d = user_group_model_dict()
    d[key] = value

    element_id = f"{db_core.database_version}:{uuid4().hex}:0"
    db_core.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=0, properties=d)]],
        None,
    )

    item = UserGroup(**d)
    saved = item.save()

    assert saved.element_id_property == element_id
    assert saved.uid == item.uid
    assert saved.__getattribute__(key) == value


def test_required_rel(db_match: MagicMock, user_group_model: UserGroup) -> None:
    db_match.cypher_query.return_value = ([], None)
    with pytest.raises(CardinalityViolation):
        user_group_model.identity_provider.all()
    with pytest.raises(CardinalityViolation):
        user_group_model.identity_provider.single()


def test_optional_rel(db_match: MagicMock, user_group_model: UserGroup) -> None:
    db_match.cypher_query.return_value = ([], None)
    assert len(user_group_model.slas.all()) == 0
    assert user_group_model.slas.single() is None


def test_linked_sla(
    db_rel_mgr: MagicMock,
    db_match: MagicMock,
    user_group_model: UserGroup,
    sla_model: SLA,
) -> None:
    assert user_group_model.slas.name
    assert user_group_model.slas.source
    assert isinstance(user_group_model.slas.source, UserGroup)
    assert user_group_model.slas.source.uid == user_group_model.uid
    assert user_group_model.slas.definition
    assert user_group_model.slas.definition["node_class"] == SLA

    r = user_group_model.slas.connect(sla_model)
    assert r is True

    db_match.cypher_query.return_value = ([[sla_model]], ["slas_r1"])
    assert len(user_group_model.slas.all()) == 1
    sla = user_group_model.slas.single()
    assert isinstance(sla, SLA)
    assert sla.uid == sla_model.uid


def test_multiple_linked_slas(
    db_rel_mgr: MagicMock,
    db_match: MagicMock,
    user_group_model: UserGroup,
    sla_model: SLA,
) -> None:
    db_match.cypher_query.return_value = (
        [[sla_model], [sla_model]],
        ["slas_r1", "slas_r2"],
    )
    assert len(user_group_model.slas.all()) == 2


@patch("neomodel.match.QueryBuilder._count", return_value=0)
def test_linked_identity_provider(
    mock_count: MagicMock,
    db_rel_mgr: MagicMock,
    db_match: MagicMock,
    user_group_model: UserGroup,
    identity_provider_model: IdentityProvider,
) -> None:
    assert user_group_model.identity_provider.name
    assert user_group_model.identity_provider.source
    assert isinstance(user_group_model.identity_provider.source, UserGroup)
    assert user_group_model.identity_provider.source.uid == user_group_model.uid
    assert user_group_model.identity_provider.definition
    assert (
        user_group_model.identity_provider.definition["node_class"] == IdentityProvider
    )

    r = user_group_model.identity_provider.connect(identity_provider_model)
    assert r is True

    db_match.cypher_query.return_value = (
        [[identity_provider_model]],
        ["identity_provider_r1"],
    )
    assert len(user_group_model.identity_provider.all()) == 1
    identity_provider = user_group_model.identity_provider.single()
    assert isinstance(identity_provider, IdentityProvider)
    assert identity_provider.uid == identity_provider_model.uid


def test_multiple_linked_identity_provider(
    db_rel_mgr: MagicMock,
    db_match: MagicMock,
    user_group_model: UserGroup,
    identity_provider_model: IdentityProvider,
) -> None:
    with patch("neomodel.match.QueryBuilder._count") as mock_count:
        mock_count.return_value = 1
        with pytest.raises(AttemptedCardinalityViolation):
            user_group_model.identity_provider.connect(identity_provider_model)

    db_match.cypher_query.return_value = (
        [[identity_provider_model], [identity_provider_model]],
        ["identity_provider_r1", "identity_provider_r2"],
    )
    with pytest.raises(CardinalityViolation):
        user_group_model.identity_provider.all()
