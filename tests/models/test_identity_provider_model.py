from typing import Any, Tuple
from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from neo4j.graph import Node
from neomodel import CardinalityViolation, RelationshipManager, RequiredProperty
from pytest_cases import parametrize, parametrize_with_cases

from fed_reg.identity_provider.models import IdentityProvider
from tests.create_dict import identity_provider_dict
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
