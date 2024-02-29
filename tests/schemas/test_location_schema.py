from typing import Any, Literal, Tuple

import pytest
from pycountry import countries
from pytest_cases import case, parametrize, parametrize_with_cases

from fed_reg.location.models import Location
from fed_reg.location.schemas import (
    LocationBase,
    LocationBasePublic,
    LocationCreate,
    LocationQuery,
    LocationRead,
    LocationReadPublic,
    LocationUpdate,
)
from fed_reg.models import BaseNode, BaseNodeCreate, BaseNodeQuery, BaseNodeRead
from tests.create_dict import location_schema_dict
from tests.utils import (
    random_country,
    random_latitude,
    random_longitude,
    random_lower_string,
)


class CaseAttr:
    @case(tags=["base_public", "update"])
    def case_none(self) -> Tuple[None, None]:
        return None, None

    @case(tags=["base_public"])
    def case_desc(self) -> Tuple[Literal["description"], str]:
        return "description", random_lower_string()

    def case_latitude(self) -> Tuple[Literal["latitude"], float]:
        return "latitude", random_latitude()

    def case_longitude(self) -> Tuple[Literal["longitude"], float]:
        return "longitude", random_longitude()

    def case_country(self) -> Tuple[Literal["country"], str]:
        return "country", random_country()

    def case_site(self) -> Tuple[Literal["site"], str]:
        return "site", random_lower_string()


class CaseInvalidAttr:
    @case(tags=["base_public", "update"])
    @parametrize(attr=["site", "country"])
    def case_attr(self, attr: str) -> Tuple[str, None]:
        return attr, None

    @case(tags=["base_public"])
    def case_country(self) -> Tuple[Literal["country"], str]:
        return "country", random_lower_string()

    @parametrize(value=[-91.0, 91.0])
    def case_latitude(self, value: float) -> Tuple[Literal["latitude"], float]:
        return "latitude", value

    @parametrize(value=[-181.0, 181.0])
    def case_longitude(self, value: float) -> Tuple[Literal["longitude"], float]:
        return "longitude", value


@parametrize_with_cases("key, value", cases=CaseAttr, has_tag=["base_public"])
def test_base_public(key: str, value: str) -> None:
    assert issubclass(LocationBasePublic, BaseNode)
    d = location_schema_dict()
    if key:
        d[key] = value
    item = LocationBasePublic(**d)
    assert item.description == d.get("description", "")
    assert item.site == d.get("site")
    assert item.country == d.get("country")


@parametrize_with_cases("key, value", cases=CaseInvalidAttr, has_tag=["base_public"])
def test_invalid_base_public(key: str, value: None) -> None:
    d = location_schema_dict()
    d[key] = value
    with pytest.raises(ValueError):
        LocationBasePublic(**d)


@parametrize_with_cases("key, value", cases=CaseAttr)
def test_base(key: str, value: Any) -> None:
    assert issubclass(LocationBase, LocationBasePublic)
    d = location_schema_dict()
    if key:
        d[key] = value
    item = LocationBase(**d)
    assert item.site == d.get("site")
    assert item.country == d.get("country")
    assert item.latitude == d.get("latitude")
    assert item.longitude == d.get("longitude")


@parametrize_with_cases("key, value", cases=CaseInvalidAttr)
def test_invalid_base(key: str, value: Any) -> None:
    d = location_schema_dict()
    d[key] = value
    with pytest.raises(ValueError):
        LocationBase(**d)


def test_create() -> None:
    assert issubclass(LocationCreate, BaseNodeCreate)
    assert issubclass(LocationCreate, LocationBase)


@parametrize_with_cases(
    "key, value", cases=[CaseInvalidAttr, CaseAttr], has_tag=["update"]
)
def test_update(key: str, value: Any) -> None:
    assert issubclass(LocationUpdate, BaseNodeCreate)
    assert issubclass(LocationUpdate, LocationBase)
    d = location_schema_dict()
    if key:
        d[key] = value
    item = LocationUpdate(**d)
    assert item.site == d.get("site")
    assert item.country == d.get("country")


def test_query() -> None:
    assert issubclass(LocationQuery, BaseNodeQuery)


@parametrize_with_cases("key, value", cases=CaseAttr, has_tag=["base_public"])
def test_read_public(location_model: Location, key: str, value: str) -> None:
    assert issubclass(LocationReadPublic, LocationBasePublic)
    assert issubclass(LocationReadPublic, BaseNodeRead)
    assert LocationReadPublic.__config__.orm_mode

    if key:
        location_model.__setattr__(key, value)
    item = LocationReadPublic.from_orm(location_model)

    assert item.uid
    assert item.uid == location_model.uid
    assert item.description == location_model.description
    assert item.site == location_model.site
    assert item.country == location_model.country


@parametrize_with_cases("key, value", cases=CaseInvalidAttr, has_tag=["base_public"])
def test_invalid_read_public(location_model: Location, key: str, value: str) -> None:
    location_model.__setattr__(key, value)
    with pytest.raises(ValueError):
        LocationReadPublic.from_orm(location_model)


@parametrize_with_cases("key, value", cases=CaseAttr)
def test_read(location_model: Location, key: str, value: Any) -> None:
    assert issubclass(LocationRead, LocationBase)
    assert issubclass(LocationRead, BaseNodeRead)
    assert LocationRead.__config__.orm_mode

    if key:
        location_model.__setattr__(key, value)
    item = LocationRead.from_orm(location_model)

    assert item.uid
    assert item.uid == location_model.uid
    assert item.description == location_model.description
    assert item.site == location_model.site
    assert item.country == location_model.country
    assert item.latitude == location_model.latitude
    assert item.longitude == location_model.longitude
    assert item.country_code == countries.search_fuzzy(item.country)[0].alpha_3


@parametrize_with_cases("key, value", cases=CaseInvalidAttr)
def test_invalid_read(location_model: Location, key: str, value: str) -> None:
    location_model.__setattr__(key, value)
    with pytest.raises(ValueError):
        LocationRead.from_orm(location_model)


# TODO Test read extended classes
