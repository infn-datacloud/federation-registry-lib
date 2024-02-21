from typing import Any, Tuple
from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from neo4j.graph import Node
from neomodel import CardinalityViolation, RelationshipManager, RequiredProperty
from pytest_cases import parametrize, parametrize_with_cases

from fed_reg.location.models import Location
from fed_reg.region.models import Region
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


def test_linked_region(
    db_rel_mgr: MagicMock,
    db_match: MagicMock,
    location_model: Location,
    region_model: Region,
) -> None:
    assert location_model.regions.name
    assert location_model.regions.source
    assert isinstance(location_model.regions.source, Location)
    assert location_model.regions.source.uid == location_model.uid
    assert location_model.regions.definition
    assert location_model.regions.definition["node_class"] == Region

    r = location_model.regions.connect(region_model)
    assert r is True

    db_match.cypher_query.return_value = ([[region_model]], ["regions_r1"])
    assert len(location_model.regions.all()) == 1
    region = location_model.regions.single()
    assert isinstance(region, Region)
    assert region.uid == region_model.uid


def test_multiple_linked_regions(
    db_rel_mgr: MagicMock,
    db_match: MagicMock,
    location_model: Location,
    region_model: Region,
) -> None:
    db_match.cypher_query.return_value = (
        [[region_model], [region_model]],
        ["regions_r1", "regions_r2"],
    )
    assert len(location_model.regions.all()) == 2
