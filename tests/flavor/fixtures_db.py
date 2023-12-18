"""Flavor specific fixtures."""
from pytest_cases import fixture, fixture_union, parametrize

from app.flavor.crud import flavor_mng
from app.flavor.models import Flavor
from app.project.models import Project
from app.provider.models import Provider
from app.provider.schemas_extended import FlavorCreateExtended
from app.region.models import Region
from app.service.models import ComputeService
from tests.flavor.utils import random_flavor_required_attr


@fixture
@parametrize(owned_projects=[0, 2])
def db_flavor_simple(
    owned_projects: int, db_compute_service_with_projects: ComputeService
) -> Flavor:
    """Fixture with standard DB Flavor.

    The flavor can be public or private based on the number of allowed projects.
    0 - Public. 1 or 2 - Private.
    """
    db_region: Region = db_compute_service_with_projects.region.single()
    db_provider: Provider = db_region.provider.single()
    projects = [i.uuid for i in db_provider.projects]
    item = {
        **random_flavor_required_attr(),
        "is_public": owned_projects == 0,
        "projects": projects[:owned_projects],
    }
    return flavor_mng.create(
        obj_in=FlavorCreateExtended(**item),
        service=db_compute_service_with_projects,
        projects=db_provider.projects,
    )


@fixture
def db_flavor_single_project(
    db_compute_service_with_single_project: ComputeService,
) -> Flavor:
    """Fixture with standard DB Flavor.

    The flavor can be public or private based on the number of allowed projects.
    0 - Public. 1 or 2 - Private.
    """
    db_region: Region = db_compute_service_with_single_project.region.single()
    db_provider: Provider = db_region.provider.single()
    db_project: Project = db_provider.projects.single()
    item = {
        **random_flavor_required_attr(),
        "is_public": False,
        "projects": [db_project.uuid],
    }
    return flavor_mng.create(
        obj_in=FlavorCreateExtended(**item),
        service=db_compute_service_with_single_project,
        projects=db_provider.projects,
    )


@fixture
def db_shared_flavor(db_region_with_compute_services: Region) -> Flavor:
    """Flavor shared by multiple services."""
    item = random_flavor_required_attr()
    for db_service in db_region_with_compute_services.services:
        db_item = flavor_mng.create(
            obj_in=FlavorCreateExtended(**item), service=db_service
        )
    assert len(db_item.services) > 1
    return db_item


db_flavor = fixture_union(
    "db_flavor",
    (db_flavor_simple, db_flavor_single_project, db_shared_flavor),
    idstyle="explicit",
)
