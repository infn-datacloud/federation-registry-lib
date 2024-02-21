from typing import Any, Tuple
from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from neo4j.graph import Node
from neomodel import CardinalityViolation, RelationshipManager, RequiredProperty
from pytest_cases import parametrize, parametrize_with_cases

from fed_reg.location.models import Location
from tests.create_dict import location_dict
from tests.utils import random_float, random_lower_string


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


@parametrize_with_cases("key, value", cases=CaseAttr)
def test_attr(db_core: MagicMock, key: str, value: Any) -> None:
    d = location_dict()
    d[key] = value

    element_id = f"{db_core.database_version}:{uuid4().hex}:0"
    db_core.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=0, properties=d)]],
        None,
    )

    item = Location(**d)
    saved = item.save()

    assert saved.element_id_property == element_id
    assert saved.uid == item.uid
    assert saved.__getattribute__(key) == value


def test_required_rel(db_match: MagicMock, location_model: Location) -> None:
    db_match.cypher_query.return_value = ([], None)
    with pytest.raises(CardinalityViolation):
        location_model.regions.all()
    with pytest.raises(CardinalityViolation):
        location_model.regions.single()
