from typing import Any, Tuple
from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from neo4j.graph import Node
from neomodel import CardinalityViolation, RelationshipManager, RequiredProperty
from pytest_cases import parametrize, parametrize_with_cases

from fed_reg.user_group.models import UserGroup
from tests.create_dict import user_group_dict
from tests.utils import random_lower_string


class CaseAttr:
    @parametrize(key=["description"])
    def case_str(self, key: str) -> Tuple[str, str]:
        return key, random_lower_string()


def test_default_attr() -> None:
    d = user_group_dict()
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
    d = user_group_dict()
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
