"""ComputeService specific fixtures."""
from pytest_cases import fixture, fixture_union, parametrize

from app.project.models import Project
from app.provider.models import Provider
from app.provider.schemas_extended import ComputeServiceCreateExtended
from app.region.models import Region
from app.service.crud import compute_service_mng
from app.service.models import ComputeService
from tests.flavor.utils import random_flavor_required_attr
from tests.image.utils import random_image_required_attr
from tests.quotas.compute_quota.utils import random_compute_quota_required_attr
from tests.services.compute_service.utils import random_compute_service_required_attr


@fixture
def db_compute_service_simple(db_region_simple: Region) -> ComputeService:
    """Fixture with standard DB ComputeService."""
    item = random_compute_service_required_attr()
    return compute_service_mng.create(
        obj_in=ComputeServiceCreateExtended(**item), region=db_region_simple
    )


@fixture
def db_compute_service_with_single_project(
    db_region_with_single_project: Region,
) -> ComputeService:
    """Fixture with standard DB ComputeService."""
    item = random_compute_service_required_attr()
    return compute_service_mng.create(
        obj_in=ComputeServiceCreateExtended(**item),
        region=db_region_with_single_project,
    )


@fixture
def db_compute_service_with_projects(db_region_with_projects: Region) -> ComputeService:
    """Fixture with standard DB ComputeService."""
    item = ComputeServiceCreateExtended(**random_compute_service_required_attr())
    return compute_service_mng.create(obj_in=item, region=db_region_with_projects)


@fixture
@parametrize(owned_quotas=[1, 2])
def db_compute_service_with_quotas(
    owned_quotas: int,
    db_region_with_projects: Region,
) -> ComputeService:
    """Fixture with standard DB ComputeService."""
    db_provider: Provider = db_region_with_projects.provider.single()
    projects = [i.uuid for i in db_provider.projects]
    quotas = []
    for project_uuid in projects:
        for i in range(owned_quotas):
            quotas.append(
                {
                    **random_compute_quota_required_attr(),
                    "per_user": i % 2,
                    "project": project_uuid,
                }
            )
    item = {**random_compute_service_required_attr(), "quotas": quotas}
    return compute_service_mng.create(
        obj_in=ComputeServiceCreateExtended(**item),
        region=db_region_with_projects,
        projects=db_provider.projects,
    )


@fixture
def db_compute_service_with_flavors(
    db_region_with_single_project: Region,
) -> ComputeService:
    """Fixture with standard DB ComputeService."""
    db_provider: Provider = db_region_with_single_project.provider.single()
    db_project: Project = db_provider.projects.single()
    item = {
        **random_compute_service_required_attr(),
        "flavors": [
            random_flavor_required_attr(),
            {
                **random_flavor_required_attr(),
                "is_public": False,
                "projects": [db_project.uuid],
            },
        ],
    }
    return compute_service_mng.create(
        obj_in=ComputeServiceCreateExtended(**item),
        region=db_region_with_single_project,
        projects=db_provider.projects,
    )


@fixture
def db_compute_service_with_images(
    db_region_with_single_project: Region,
) -> ComputeService:
    """Fixture with standard DB ComputeService."""
    db_provider: Provider = db_region_with_single_project.provider.single()
    db_project: Project = db_provider.projects.single()
    item = {
        **random_compute_service_required_attr(),
        "images": [
            random_image_required_attr(),
            {
                **random_image_required_attr(),
                "is_public": False,
                "projects": [db_project.uuid],
            },
        ],
    }
    return compute_service_mng.create(
        obj_in=ComputeServiceCreateExtended(**item),
        region=db_region_with_single_project,
        projects=db_provider.projects,
    )


db_compute_service = fixture_union(
    "db_compute_service",
    (
        db_compute_service_simple,
        db_compute_service_with_flavors,
        db_compute_service_with_images,
        db_compute_service_with_quotas,
    ),
    idstyle="explicit",
)
