"""Provider specific fixtures."""
from typing import Any, Dict, Generator

from pytest_cases import fixture, fixture_union

from app.provider.crud import provider_mng
from app.provider.models import Provider
from app.provider.schemas_extended import (
    ProviderCreateExtended,
)
from tests.provider.utils import random_provider_required_attr


@fixture
def db_provider_simple(setup_and_teardown_db: Generator) -> Provider:
    """Fixture with standard DB Provider."""
    item = ProviderCreateExtended(**random_provider_required_attr())
    return provider_mng.create(obj_in=item)


@fixture
def db_provider_with_regions(
    setup_and_teardown_db: Generator,
    provider_create_data_with_regions: Dict[str, Any],
) -> Provider:
    """Fixture with standard DB Provider."""
    item = ProviderCreateExtended(**provider_create_data_with_regions)
    return provider_mng.create(obj_in=item)


@fixture
def db_provider_with_single_project(
    setup_and_teardown_db: Generator,
    provider_create_data_with_single_project: Dict[str, Any],
) -> Provider:
    """Fixture with standard DB Provider."""
    item = ProviderCreateExtended(**provider_create_data_with_single_project)
    return provider_mng.create(obj_in=item)


@fixture
def db_provider_with_projects(
    setup_and_teardown_db: Generator,
    provider_create_data_with_projects: Dict[str, Any],
) -> Provider:
    """Fixture with standard DB Provider."""
    item = ProviderCreateExtended(**provider_create_data_with_projects)
    return provider_mng.create(obj_in=item)


@fixture
def db_provider_with_idps(
    setup_and_teardown_db: Generator, provider_create_data_with_idps: Dict[str, Any]
) -> Provider:
    """Fixture with standard DB Provider."""
    item = ProviderCreateExtended(**provider_create_data_with_idps)
    return provider_mng.create(obj_in=item)


db_provider = fixture_union(
    "db_provider",
    (
        db_provider_simple,
        db_provider_with_regions,
        db_provider_with_projects,
        db_provider_with_idps,
    ),
    idstyle="explicit",
)
