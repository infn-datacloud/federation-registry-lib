from typing import Any

from pycountry import countries
from pytest_cases import parametrize_with_cases

from fed_reg.location.models import Location
from fed_reg.location.schemas import (
    LocationBase,
    LocationBasePublic,
    LocationRead,
    LocationReadPublic,
    LocationUpdate,
)
from tests.create_dict import location_schema_dict


@parametrize_with_cases("key, value", has_tag="base_public")
def test_base_public(key: str, value: str) -> None:
    d = location_schema_dict()
    if key:
        d[key] = value
    item = LocationBasePublic(**d)
    assert item.description == d.get("description", "")
    assert item.site == d.get("site")
    assert item.country == d.get("country")


@parametrize_with_cases("key, value", has_tag="base")
def test_base(key: str, value: Any) -> None:
    d = location_schema_dict()
    if key:
        d[key] = value
    item = LocationBase(**d)
    assert item.site == d.get("site")
    assert item.country == d.get("country")
    assert item.latitude == d.get("latitude")
    assert item.longitude == d.get("longitude")


@parametrize_with_cases("key, value", has_tag="base_public")
def test_read_public(location_model: Location, key: str, value: str) -> None:
    if key:
        location_model.__setattr__(key, value)
    item = LocationReadPublic.from_orm(location_model)

    assert item.uid
    assert item.uid == location_model.uid
    assert item.description == location_model.description
    assert item.site == location_model.site
    assert item.country == location_model.country


@parametrize_with_cases("key, value", has_tag="base")
def test_read(location_model: Location, key: str, value: Any) -> None:
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


@parametrize_with_cases("key, value", has_tag="update")
def test_update(key: str, value: Any) -> None:
    d = location_schema_dict()
    if key:
        d[key] = value
    item = LocationUpdate(**d)
    assert item.site == d.get("site")
    assert item.country == d.get("country")


# @parametrize_with_cases("model", cases=CaseDBInstance, has_tag="location")
# @parametrize_with_cases("public", cases=CasePublic)
# def test_read_extended(model: Location, public: bool) -> None:
#     if public:
#         cls = LocationReadPublic
#         cls_ext = LocationReadExtendedPublic
#         reg_cls = RegionReadPublic
#     else:
#         cls = LocationRead
#         cls_ext = LocationReadExtended
#         reg_cls = RegionRead

#     assert issubclass(cls_ext, cls)
#     assert cls_ext.__config__.orm_mode

#     item = cls_ext.from_orm(model)

#     assert len(item.regions) == len(model.regions.all())

#     assert all([isinstance(i, reg_cls) for i in item.regions])
