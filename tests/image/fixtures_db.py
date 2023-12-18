"""Image specific fixtures."""
from pytest_cases import fixture, fixture_union, parametrize

from app.image.crud import image_mng
from app.image.models import Image
from app.project.models import Project
from app.provider.models import Provider
from app.provider.schemas_extended import ImageCreateExtended
from app.region.models import Region
from app.service.models import ComputeService
from tests.image.utils import random_image_required_attr


@fixture
@parametrize(owned_projects=[0, 2])
def db_image_simple(
    owned_projects: int, db_compute_service_with_projects: ComputeService
) -> Image:
    """Fixture with standard DB Image.

    The image can be public or private based on the number of allowed projects.
    0 - Public. 1 or 2 - Private.
    """
    db_region: Region = db_compute_service_with_projects.region.single()
    db_provider: Provider = db_region.provider.single()
    projects = [i.uuid for i in db_provider.projects]
    item = {
        **random_image_required_attr(),
        "is_public": owned_projects == 0,
        "projects": projects[:owned_projects],
    }
    return image_mng.create(
        obj_in=ImageCreateExtended(**item),
        service=db_compute_service_with_projects,
        projects=db_provider.projects,
    )


@fixture
def db_image_single_project(
    db_compute_service_with_single_project: ComputeService,
) -> Image:
    """Fixture with standard DB Image.

    The image can be public or private based on the number of allowed projects.
    0 - Public. 1 or 2 - Private.
    """
    db_region: Region = db_compute_service_with_single_project.region.single()
    db_provider: Provider = db_region.provider.single()
    db_project: Project = db_provider.projects.single()
    item = {
        **random_image_required_attr(),
        "is_public": False,
        "projects": [db_project.uuid],
    }
    return image_mng.create(
        obj_in=ImageCreateExtended(**item),
        service=db_compute_service_with_single_project,
        projects=db_provider.projects,
    )


@fixture
def db_shared_image(
    db_region_with_compute_services: Region,
) -> Image:
    """Image shared by multiple services."""
    item = random_image_required_attr()
    for db_service in db_region_with_compute_services.services:
        db_item = image_mng.create(
            obj_in=ImageCreateExtended(**item), service=db_service
        )
    assert len(db_item.services) > 1
    return db_item


db_image = fixture_union(
    "db_image",
    (db_image_simple, db_image_single_project, db_shared_image),
    idstyle="explicit",
)
