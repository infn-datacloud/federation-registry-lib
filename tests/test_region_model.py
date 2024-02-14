from typing import Any, Dict, Tuple
from unittest.mock import Mock, PropertyMock, patch
from uuid import uuid4

import pytest
from neo4j.graph import Node
from neomodel import CardinalityViolation, RelationshipManager, RequiredProperty
from pytest_cases import parametrize, parametrize_with_cases

from fed_reg.region.models import Region
from tests.common.utils import random_lower_string


class CaseAttr:
    @parametrize(key=["description"])
    def case_str(self, key: str) -> Tuple[str, str]:
        return key, random_lower_string()


def region_dict() -> Dict[str, str]:
    return {"name": random_lower_string()}


def test_default_attr() -> None:
    d = region_dict()
    item = Region(**d)
    assert item.uid is not None
    assert item.description == ""
    assert item.name == d.get("name")
    assert isinstance(item.location, RelationshipManager)
    assert isinstance(item.provider, RelationshipManager)
    assert isinstance(item.services, RelationshipManager)


def test_missing_attr() -> None:
    item = Region()
    with pytest.raises(RequiredProperty):
        item.save()


@patch("neomodel.core.db")
@parametrize_with_cases("key, value", cases=CaseAttr)
def test_attr(mock_db: Mock, key: str, value: Any) -> None:
    d = region_dict()
    d[key] = value

    db_version = "5"
    type(mock_db).database_version = PropertyMock(return_value=db_version)
    element_id = f"{db_version}:{uuid4().hex}:0"
    mock_db.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=0, properties=d)]],
        None,
    )

    item = Region(**d)
    saved = item.save()

    assert saved.element_id_property == element_id
    assert saved.uid == item.uid
    assert saved.__getattribute__(key) == value


def test_required_rel() -> None:
    item = Region(**region_dict())
    with pytest.raises(CardinalityViolation):
        item.provider.all()
    with pytest.raises(CardinalityViolation):
        item.provider.single()


def test_optional_rel() -> None:
    item = Region(**region_dict())
    assert len(item.location.all()) == 0
    assert item.location.single() is None
    assert len(item.services.all()) == 0
    assert item.services.single() is None
