"""Region specific fixtures."""
from pytest_cases import fixture, fixture_union, parametrize

from app.provider.models import Provider
from app.provider.schemas_extended import (
    RegionCreateExtended,
)
from app.region.crud import region_mng
from app.region.models import Region
from tests.location.utils import random_location_required_attr
from tests.region.utils import random_region_required_attr
from tests.services.block_storage_service.utils import (
    random_block_storage_service_required_attr,
)
from tests.services.compute_service.utils import random_compute_service_required_attr
from tests.services.identity_service.utils import random_identity_service_required_attr
from tests.services.network_service.utils import random_network_service_required_attr


@fixture
def db_region_simple(db_provider_simple: Provider) -> Region:
    """Fixture with standard DB Region."""
    item = RegionCreateExtended(**random_region_required_attr())
    return region_mng.create(obj_in=item, provider=db_provider_simple)


@fixture
def db_region_with_single_project(db_provider_with_single_project: Provider) -> Region:
    """Fixture with standard DB Region."""
    item = RegionCreateExtended(**random_region_required_attr())
    return region_mng.create(obj_in=item, provider=db_provider_with_single_project)


@fixture
def db_region_with_projects(db_provider_with_projects: Provider) -> Region:
    """Fixture with standard DB Region."""
    item = RegionCreateExtended(**random_region_required_attr())
    return region_mng.create(obj_in=item, provider=db_provider_with_projects)


@fixture
def db_region_with_location(
    db_provider_simple: Provider,
) -> Region:
    """Fixture with standard DB Region."""
    item = RegionCreateExtended(
        {**random_region_required_attr(), "location": random_location_required_attr()}
    )
    return region_mng.create(obj_in=item, provider=db_provider_simple)


@fixture
@parametrize(owned_services=[1, 2])
def db_region_with_block_storage_services(
    owned_services: int,
    db_provider_simple: Provider,
) -> Region:
    """Fixture with standard DB Region."""
    services = []
    for _ in range(owned_services):
        services.append(random_block_storage_service_required_attr())
    item = RegionCreateExtended(
        **random_region_required_attr(), block_storage_services=services
    )
    return region_mng.create(obj_in=item, provider=db_provider_simple)


@fixture
@parametrize(owned_services=[1, 2])
def db_region_with_compute_services(
    owned_services: int,
    db_provider_simple: Provider,
) -> Region:
    """Fixture with standard DB Region."""
    services = []
    for _ in range(owned_services):
        services.append(random_compute_service_required_attr())
    item = RegionCreateExtended(
        **random_region_required_attr(), compute_services=services
    )
    return region_mng.create(obj_in=item, provider=db_provider_simple)


@fixture
@parametrize(owned_services=[1, 2])
def db_region_with_identity_services(
    owned_services: int,
    db_provider_simple: Provider,
) -> Region:
    """Fixture with standard DB Region."""
    services = []
    for _ in range(owned_services):
        services.append(random_identity_service_required_attr())
    item = RegionCreateExtended(
        **random_region_required_attr(), identity_services=services
    )
    return region_mng.create(obj_in=item, provider=db_provider_simple)


@fixture
@parametrize(owned_services=[1, 2])
def db_region_with_network_services(
    owned_services: int,
    db_provider_simple: Provider,
) -> Region:
    """Fixture with standard DB Region."""
    services = []
    for _ in range(owned_services):
        services.append(random_network_service_required_attr())
    item = RegionCreateExtended(
        **random_region_required_attr(), network_services=services
    )
    return region_mng.create(obj_in=item, provider=db_provider_simple)


db_region = fixture_union(
    "db_region",
    (
        db_region_simple,
        db_region_with_location,
        db_region_with_block_storage_services,
        db_region_with_compute_services,
        db_region_with_identity_services,
        db_region_with_network_services,
    ),
    idstyle="explicit",
)
