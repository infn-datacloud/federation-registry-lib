from pytest_cases import parametrize_with_cases

from fedreg.core import BaseReadPrivateExtended, BaseReadPublicExtended
from fedreg.location.models import Location
from fedreg.location.schemas import LocationRead, LocationReadPublic
from fedreg.location.schemas_extended import (
    LocationReadExtended,
    LocationReadExtendedPublic,
)
from fedreg.region.models import Region


def test_class_inheritance():
    assert issubclass(LocationReadExtended, BaseReadPrivateExtended)
    assert issubclass(LocationReadExtended, LocationRead)
    assert LocationReadExtended.__fields__["schema_type"].default == "private_extended"
    assert LocationReadExtended.__config__.orm_mode is True

    assert issubclass(LocationReadExtendedPublic, BaseReadPublicExtended)
    assert issubclass(LocationReadExtendedPublic, LocationReadPublic)
    assert (
        LocationReadExtendedPublic.__fields__["schema_type"].default
        == "public_extended"
    )
    assert LocationReadExtendedPublic.__config__.orm_mode is True


@parametrize_with_cases("regions", has_tag="regions")
def test_read_ext(location_model: Location, regions: list[Region]) -> None:
    for region in regions:
        location_model.regions.connect(region)

    item = LocationReadExtendedPublic.from_orm(location_model)
    assert len(item.regions) == len(regions)

    item = LocationReadExtended.from_orm(location_model)
    assert len(item.regions) == len(regions)
