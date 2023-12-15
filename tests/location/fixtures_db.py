"""Location specific fixtures."""
from typing import Any, Dict

from pytest_cases import fixture, fixture_union

from app.location.crud import location_mng
from app.location.models import Location
from app.provider.models import Provider
from app.provider.schemas_extended import LocationCreate
from app.region.models import Region


@fixture
def db_location_simple(
    location_create_mandatory_data: Dict[str, Any], db_region_simple: Region
) -> Location:
    """Fixture with standard DB Location."""
    item = LocationCreate(**location_create_mandatory_data)
    return location_mng.create(obj_in=item, region=db_region_simple)


# TODO Evaluate if this case should be splitted.
@fixture
def db_shared_location(
    db_location_simple: Location, db_provider_with_regions: Provider
) -> Location:
    """Location shared within multiple regions.

    This location is shared between regions belonging to the same providers and regions
    belonging to another provider.
    """
    item = LocationCreate(**db_location_simple.__dict__)
    for db_region in db_provider_with_regions.regions:
        db_item = location_mng.create(obj_in=item, region=db_region)
    assert len(db_item.regions) > 1
    return db_item


db_location = fixture_union(
    "db_location", (db_location_simple, db_shared_location), idstyle="explicit"
)
