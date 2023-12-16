"""Region specific fixtures."""
from typing import Any, Dict

from pytest_cases import fixture, fixture_union

from app.provider.models import Provider
from app.provider.schemas_extended import (
    RegionCreateExtended,
)
from app.region.crud import region_mng
from app.region.models import Region


@fixture
def db_region_simple(
    region_create_mandatory_data: Dict[str, Any],
    db_provider_simple: Provider,
) -> Region:
    """Fixture with standard DB Region."""
    item = RegionCreateExtended(**region_create_mandatory_data)
    return region_mng.create(obj_in=item, provider=db_provider_simple)


@fixture
def db_region_with_single_project(
    region_create_mandatory_data: Dict[str, Any],
    db_provider_with_single_project: Provider,
) -> Region:
    """Fixture with standard DB Region."""
    item = RegionCreateExtended(**region_create_mandatory_data)
    return region_mng.create(obj_in=item, provider=db_provider_with_single_project)


@fixture
def db_region_with_projects(
    region_create_mandatory_data: Dict[str, Any],
    db_provider_with_projects: Provider,
) -> Region:
    """Fixture with standard DB Region."""
    item = RegionCreateExtended(**region_create_mandatory_data)
    return region_mng.create(obj_in=item, provider=db_provider_with_projects)


@fixture
def db_region_with_location(
    region_create_data_with_location: Dict[str, Any],
    db_provider_simple: Provider,
) -> Region:
    """Fixture with standard DB Region."""
    item = RegionCreateExtended(**region_create_data_with_location)
    return region_mng.create(obj_in=item, provider=db_provider_simple)


@fixture
def db_region_with_block_storage_services(
    region_create_data_with_block_storage_services: Dict[str, Any],
    db_provider_simple: Provider,
) -> Region:
    """Fixture with standard DB Region."""
    item = RegionCreateExtended(**region_create_data_with_block_storage_services)
    return region_mng.create(obj_in=item, provider=db_provider_simple)


@fixture
def db_region_with_compute_services(
    region_create_data_with_compute_services: Dict[str, Any],
    db_provider_simple: Provider,
) -> Region:
    """Fixture with standard DB Region."""
    item = RegionCreateExtended(**region_create_data_with_compute_services)
    return region_mng.create(obj_in=item, provider=db_provider_simple)


@fixture
def db_region_with_identity_services(
    region_create_data_with_identity_services: Dict[str, Any],
    db_provider_simple: Provider,
) -> Region:
    """Fixture with standard DB Region."""
    item = RegionCreateExtended(**region_create_data_with_identity_services)
    return region_mng.create(obj_in=item, provider=db_provider_simple)


@fixture
def db_region_with_network_services(
    region_create_data_with_network_services: Dict[str, Any],
    db_provider_simple: Provider,
) -> Region:
    """Fixture with standard DB Region."""
    item = RegionCreateExtended(**region_create_data_with_network_services)
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
