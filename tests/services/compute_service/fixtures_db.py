"""ComputeService specific fixtures."""
from typing import Any, Dict
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
from tests.utils.utils import random_lower_string

relationships_num = [1, 2]


@fixture
def db_compute_service_simple(
    compute_service_create_mandatory_data: Dict[str, Any], db_region_simple: Region
) -> ComputeService:
    """Fixture with standard DB ComputeService."""
    item = ComputeServiceCreateExtended(**compute_service_create_mandatory_data)
    return compute_service_mng.create(obj_in=item, region=db_region_simple)


@fixture
def db_compute_service_with_single_project(
    compute_service_create_mandatory_data: Dict[str, Any],
    db_region_with_single_project: Region,
) -> ComputeService:
    """Fixture with standard DB ComputeService."""
    item = ComputeServiceCreateExtended(**compute_service_create_mandatory_data)
    return compute_service_mng.create(obj_in=item, region=db_region_with_single_project)


@fixture
def db_compute_service_with_projects(
    compute_service_create_mandatory_data: Dict[str, Any],
    db_region_with_projects: Region,
) -> ComputeService:
    """Fixture with standard DB ComputeService."""
    item = ComputeServiceCreateExtended(**compute_service_create_mandatory_data)
    return compute_service_mng.create(obj_in=item, region=db_region_with_projects)


@fixture
@parametrize(owned_quotas=relationships_num)
def db_compute_service_with_quotas(
    owned_quotas: int,
    compute_service_create_mandatory_data: Dict[str, Any],
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
        **compute_service_create_mandatory_data, quotas=quotas
    )
    return compute_service_mng.create(
        obj_in=item, region=db_region_with_projects, projects=db_provider.projects
    )


@fixture
@parametrize(owned_flavors=relationships_num)
def db_compute_service_with_flavors(
    owned_flavors: int,
    compute_service_create_mandatory_data: Dict[str, Any],
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
        **compute_service_create_mandatory_data, flavors=flavors
    )
    return compute_service_mng.create(
        obj_in=item, region=db_region_with_projects, projects=db_provider.projects
    )


@fixture
@parametrize(owned_images=relationships_num)
def db_compute_service_with_images(
    owned_images: int,
    compute_service_create_mandatory_data: Dict[str, Any],
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
        **compute_service_create_mandatory_data, images=images
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
