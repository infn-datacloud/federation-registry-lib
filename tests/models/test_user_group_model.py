from typing import Any, Tuple
from unittest.mock import Mock, PropertyMock, patch
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


@patch("neomodel.core.db")
@parametrize_with_cases("key, value", cases=CaseAttr)
def test_attr(mock_db: Mock, key: str, value: Any) -> None:
    d = user_group_dict()
    d[key] = value

    db_version = "5"
    type(mock_db).database_version = PropertyMock(return_value=db_version)
    element_id = f"{db_version}:{uuid4().hex}:0"
    mock_db.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=0, properties=d)]],
        None,
    )

    item = UserGroup(**d)
    saved = item.save()

    assert saved.element_id_property == element_id
    assert saved.uid == item.uid
    assert saved.__getattribute__(key) == value


@patch("neomodel.match.db")
def test_required_rel(mock_db: Mock) -> None:
    db_version = "5"
    type(mock_db).database_version = PropertyMock(return_value=db_version)
    mock_db.cypher_query.return_value = ([], None)

    item = UserGroup(**user_group_dict())
    with pytest.raises(CardinalityViolation):
        item.identity_provider.all()
    with pytest.raises(CardinalityViolation):
        item.identity_provider.single()


@patch("neomodel.match.db")
def test_optional_rel(mock_db: Mock) -> None:
    db_version = "5"
    type(mock_db).database_version = PropertyMock(return_value=db_version)
    mock_db.cypher_query.return_value = ([], None)

    item = UserGroup(**user_group_dict())
    assert len(item.slas.all()) == 0
    assert item.slas.single() is None
