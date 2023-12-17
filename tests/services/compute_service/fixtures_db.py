"""ComputeService specific fixtures."""
from uuid import uuid4

from pytest_cases import fixture, fixture_union, parametrize

from app.provider.models import Provider
from app.provider.schemas_extended import (
    ComputeQuotaCreateExtended,
    ComputeServiceCreateExtended,
    FlavorCreateExtended,
    ImageCreateExtended,
)
from app.region.models import Region
from app.service.crud import compute_service_mng
from app.service.models import ComputeService
from tests.common.utils import random_lower_string
from tests.services.compute_service.utils import random_compute_service_required_attr

relationships_num = [1, 2]


@fixture
def db_compute_service_simple(db_region_simple: Region) -> ComputeService:
    """Fixture with standard DB ComputeService."""
    item = ComputeServiceCreateExtended(**random_compute_service_required_attr())
    return compute_service_mng.create(obj_in=item, region=db_region_simple)


@fixture
def db_compute_service_with_single_project(
    db_region_with_single_project: Region,
) -> ComputeService:
    """Fixture with standard DB ComputeService."""
    item = ComputeServiceCreateExtended(**random_compute_service_required_attr())
    return compute_service_mng.create(obj_in=item, region=db_region_with_single_project)


@fixture
def db_compute_service_with_projects(
    db_region_with_projects: Region,
) -> ComputeService:
    """Fixture with standard DB ComputeService."""
    item = ComputeServiceCreateExtended(**random_compute_service_required_attr())
    return compute_service_mng.create(obj_in=item, region=db_region_with_projects)


@fixture
@parametrize(owned_quotas=relationships_num)
def db_compute_service_with_quotas(
    owned_quotas: int,
    db_region_with_projects: Region,
) -> ComputeService:
    """Fixture with standard DB ComputeService."""
    db_provider: Provider = db_region_with_projects.provider.single()
    projects = [i.uuid for i in db_provider.projects]
    quotas = []
    for i in projects:
        for n in range(owned_quotas):
            quotas.append(ComputeQuotaCreateExtended(per_user=n % 2, project=i))
    item = ComputeServiceCreateExtended(
        **random_compute_service_required_attr(), quotas=quotas
    )
    return compute_service_mng.create(
        obj_in=item, region=db_region_with_projects, projects=db_provider.projects
    )


@fixture
@parametrize(owned_flavors=relationships_num)
def db_compute_service_with_flavors(
    owned_flavors: int,
    db_region_with_projects: Region,
) -> ComputeService:
    """Fixture with standard DB ComputeService."""
    db_provider: Provider = db_region_with_projects.provider.single()
    projects = [i.uuid for i in db_provider.projects]
    flavors = [FlavorCreateExtended(name=random_lower_string(), uuid=uuid4())]
    for i in projects:
        for _ in range(owned_flavors):
            flavors.append(
                FlavorCreateExtended(
                    name=random_lower_string(),
                    uuid=uuid4(),
                    is_public=False,
                    projects=[i],
                )
            )
    item = ComputeServiceCreateExtended(
        **random_compute_service_required_attr(), flavors=flavors
    )
    return compute_service_mng.create(
        obj_in=item, region=db_region_with_projects, projects=db_provider.projects
    )


@fixture
@parametrize(owned_images=relationships_num)
def db_compute_service_with_images(
    owned_images: int,
    db_region_with_projects: Region,
) -> ComputeService:
    """Fixture with standard DB ComputeService."""
    db_provider: Provider = db_region_with_projects.provider.single()
    projects = [i.uuid for i in db_provider.projects]
    images = [ImageCreateExtended(name=random_lower_string(), uuid=uuid4())]
    for i in projects:
        for _ in range(owned_images):
            images.append(
                ImageCreateExtended(
                    name=random_lower_string(),
                    uuid=uuid4(),
                    is_public=False,
                    projects=[i],
                )
            )
    item = ComputeServiceCreateExtended(
        **random_compute_service_required_attr(), images=images
    )
    return compute_service_mng.create(
        obj_in=item, region=db_region_with_projects, projects=db_provider.projects
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
