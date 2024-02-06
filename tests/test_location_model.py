from typing import Any, Dict, Tuple
from unittest.mock import Mock, PropertyMock, patch
from uuid import uuid4

import pytest
from neo4j.graph import Node
from neomodel import CardinalityViolation, RelationshipManager, RequiredProperty
from pytest_cases import parametrize, parametrize_with_cases

from app.location.models import Location
from tests.common.utils import random_float, random_lower_string


class CaseMissing:
    @parametrize(value=["site", "country"])
    def case_missing(self, value: str) -> str:
        return value


class CaseAttr:
    @parametrize(key=["description"])
    def case_str(self, key: str) -> Tuple[str, str]:
        return key, random_lower_string()

    @parametrize(key=["latitude", "longitude"])
    def case_float(self, key: str) -> Tuple[str, float]:
        return key, random_float(0, 100)


def location_dict() -> Dict[str, str]:
    return {"site": random_lower_string(), "country": random_lower_string()}


def test_default_attr() -> None:
    d = location_dict()
    item = Location(**d)
    assert item.uid is not None
    assert item.description == ""
    assert item.site == d.get("site")
    assert item.country == d.get("country")
    assert item.latitude is None
    assert item.longitude is None
    assert isinstance(item.regions, RelationshipManager)


@parametrize_with_cases("missing_attr", cases=CaseMissing)
def test_missing_attr(missing_attr: str) -> None:
    d = location_dict()
    d[missing_attr] = None
    item = Location(**d)
    with pytest.raises(RequiredProperty):
        item.save()


@patch("neomodel.core.db")
@parametrize_with_cases("key, value", cases=CaseAttr)
def test_attr(mock_db: Mock, key: str, value: Any) -> None:
    d = location_dict()
    d[key] = value

    db_version = "5"
    type(mock_db).database_version = PropertyMock(return_value=db_version)
    element_id = f"{db_version}:{uuid4().hex}:0"
    mock_db.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=0, properties=d)]],
        None,
    )

    item = Location(**d)
    saved = item.save()

    assert saved.element_id_property == element_id
    assert saved.uid == item.uid
    assert saved.__getattribute__(key) == value


def test_required_rel() -> None:
    item = Location(**location_dict())
    with pytest.raises(CardinalityViolation):
        item.regions.all()
    with pytest.raises(CardinalityViolation):
        item.regions.single()
