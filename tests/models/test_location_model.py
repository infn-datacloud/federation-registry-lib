from typing import Any, Tuple

import pytest
from neomodel import CardinalityViolation, RelationshipManager, RequiredProperty
from pytest_cases import parametrize, parametrize_with_cases

from fed_reg.location.models import Location
from fed_reg.region.models import Region
from tests.create_dict import location_model_dict
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
    d = location_model_dict()
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
    d = location_model_dict()
    d[missing_attr] = None
    item = Location(**d)
    with pytest.raises(RequiredProperty):
        item.save()


@parametrize_with_cases("key, value", cases=CaseAttr)
def test_attr(key: str, value: Any) -> None:
    d = location_model_dict()
    d[key] = value

    item = Location(**d)
    saved = item.save()

    assert saved.element_id_property
    assert saved.uid == item.uid
    assert saved.__getattribute__(key) == value


def test_required_rel(location_model: Location) -> None:
    with pytest.raises(CardinalityViolation):
        location_model.regions.all()
    with pytest.raises(CardinalityViolation):
        location_model.regions.single()


def test_linked_region(location_model: Location, region_model: Region) -> None:
    assert location_model.regions.name
    assert location_model.regions.source
    assert isinstance(location_model.regions.source, Location)
    assert location_model.regions.source.uid == location_model.uid
    assert location_model.regions.definition
    assert location_model.regions.definition["node_class"] == Region

    r = location_model.regions.connect(region_model)
    assert r is True

    assert len(location_model.regions.all()) == 1
    region = location_model.regions.single()
    assert isinstance(region, Region)
    assert region.uid == region_model.uid


def test_multiple_linked_regions(
    location_model: Location, region_model: Region
) -> None:
    location_model.regions.connect(region_model)
    location_model.regions.connect(region_model)
    assert len(location_model.regions.all()) == 2
