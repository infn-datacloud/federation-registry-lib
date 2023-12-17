"""Location specific fixtures."""
from pytest_cases import fixture, fixture_union

from app.location.crud import location_mng
from app.location.models import Location
from app.provider.models import Provider
from app.provider.schemas_extended import LocationCreate, RegionCreateExtended
from app.region.crud import region_mng
from app.region.models import Region
from tests.location.utils import random_location_required_attr
from tests.region.utils import random_region_required_attr


@fixture
def db_location_simple(db_region_simple: Region) -> Location:
    """Fixture with standard DB Location."""
    item = LocationCreate(**random_location_required_attr())
    return location_mng.create(obj_in=item, region=db_region_simple)


@fixture
def db_shared_location(
    db_provider_simple: Provider, db_provider_with_regions: Provider
) -> Location:
    """Location shared within multiple regions.

    This location is shared between regions belonging to the same providers and regions
    belonging to another provider.
    """
    item = LocationCreate(**random_location_required_attr())
    db_regions = db_provider_with_regions.regions
    if len(db_provider_with_regions.regions) == 1:
        db_regions = [
            *db_regions,
            region_mng.create(
                obj_in=RegionCreateExtended(**random_region_required_attr()),
                provider=db_provider_simple,
            ),
        ]
    for db_region in db_regions:
        db_item = location_mng.create(obj_in=item, region=db_region)
    assert len(db_item.regions) > 1
    return db_item


db_location = fixture_union(
    "db_location", (db_location_simple, db_shared_location), idstyle="explicit"
)
