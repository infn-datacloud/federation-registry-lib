from typing import Any, Dict, List, Literal, Tuple
from unittest.mock import Mock, PropertyMock, patch
from uuid import uuid4

import pytest
from neo4j.graph import Node
from neomodel import RelationshipManager, RequiredProperty
from pytest_cases import parametrize, parametrize_with_cases

from fed_reg.provider.models import Provider
from tests.utils import random_lower_string


class CaseMissing:
    @parametrize(value=["name", "type"])
    def case_missing(self, value: str) -> str:
        return value


class CaseAttr:
    @parametrize(key=["description", "status"])
    def case_str(self, key: str) -> Tuple[str, str]:
        return key, random_lower_string()

    @parametrize(key=["is_public"])
    def case_bool(self, key: str) -> Tuple[str, Literal[True]]:
        return key, True

    @parametrize(key=["empty", "full"])
    def case_list_str(self, key: str) -> Tuple[str, List[str]]:
        if key == "empty":
            return key, []
        return key, [random_lower_string()]


def provider_dict() -> Dict[str, str]:
    return {"name": random_lower_string(), "type": random_lower_string()}


def test_default_attr() -> None:
    d = provider_dict()
    item = Provider(**d)
    assert item.uid is not None
    assert item.description == ""
    assert item.name == d.get("name")
    assert item.type == d.get("type")
    assert item.is_public is False
    assert item.status is None
    assert item.support_emails is None
    assert isinstance(item.projects, RelationshipManager)
    assert isinstance(item.regions, RelationshipManager)
    assert isinstance(item.identity_providers, RelationshipManager)


@parametrize_with_cases("missing_attr", cases=CaseMissing)
def test_missing_attr(missing_attr: str) -> None:
    d = provider_dict()
    d[missing_attr] = None
    item = Provider(**d)
    with pytest.raises(RequiredProperty):
        item.save()


@patch("neomodel.core.db")
@parametrize_with_cases("key, value", cases=CaseAttr)
def test_attr(mock_db: Mock, key: str, value: Any) -> None:
    d = provider_dict()
    d[key] = value

    db_version = "5"
    type(mock_db).database_version = PropertyMock(return_value=db_version)
    element_id = f"{db_version}:{uuid4().hex}:0"
    mock_db.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=0, properties=d)]],
        None,
    )

    item = Provider(**d)
    saved = item.save()

    assert saved.element_id_property == element_id
    assert saved.uid == item.uid
    assert saved.__getattribute__(key) == value


@patch("neomodel.match.db")
def test_optional_rel(mock_db: Mock) -> None:
    db_version = "5"
    type(mock_db).database_version = PropertyMock(return_value=db_version)
    mock_db.cypher_query.return_value = ([], None)

    item = Provider(**provider_dict())
    assert len(item.identity_providers.all()) == 0
    assert item.identity_providers.single() is None
    assert len(item.projects.all()) == 0
    assert item.projects.single() is None
    assert len(item.regions.all()) == 0
    assert item.regions.single() is None
