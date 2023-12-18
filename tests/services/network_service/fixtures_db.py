"""NetworkService specific fixtures."""
from pytest_cases import fixture, fixture_union, parametrize

from app.project.models import Project
from app.provider.models import Provider
from app.provider.schemas_extended import NetworkServiceCreateExtended
from app.region.models import Region
from app.service.crud import network_service_mng
from app.service.models import NetworkService
from tests.network.utils import random_network_required_attr
from tests.quotas.network_quota.utils import random_network_quota_required_attr
from tests.services.network_service.utils import random_network_service_required_attr


@fixture
def db_network_service_simple(db_region_simple: Region) -> NetworkService:
    """Fixture with standard DB NetworkService."""
    item = NetworkServiceCreateExtended(**random_network_service_required_attr())
    return network_service_mng.create(obj_in=item, region=db_region_simple)


@fixture
def db_network_service_with_single_project(
    db_region_with_single_project: Region,
) -> NetworkService:
    """Fixture with standard DB NetworkService."""
    item = NetworkServiceCreateExtended(**random_network_service_required_attr())
    return network_service_mng.create(obj_in=item, region=db_region_with_single_project)


@fixture
@parametrize(owned_quotas=[1, 2])
def db_network_service_with_quotas(
    owned_quotas: int, db_region_with_projects: Region
) -> NetworkService:
    """Fixture with standard DB NetworkService."""
    db_provider: Provider = db_region_with_projects.provider.single()
    projects = [i.uuid for i in db_provider.projects]
    quotas = []
    for project_uuid in projects:
        for i in range(owned_quotas):
            quotas.append(
                {
                    **random_network_quota_required_attr(),
                    "per_user": i % 2,
                    "project": project_uuid,
                }
            )
    item = {**random_network_service_required_attr(), "quotas": quotas}
    return network_service_mng.create(
        obj_in=NetworkServiceCreateExtended(**item),
        region=db_region_with_projects,
        projects=db_provider.projects,
    )


@fixture
def db_network_service_with_networks(
    db_region_with_single_project: Region,
) -> NetworkService:
    """Fixture with standard DB NetworkService."""
    db_provider: Provider = db_region_with_single_project.provider.single()
    db_project: Project = db_provider.projects.single()
    item = {
        **random_network_service_required_attr(),
        "networks": [
            random_network_required_attr(),
            {
                **random_network_required_attr(),
                "is_shared": False,
                "project": db_project.uuid,
            },
        ],
    }
    return network_service_mng.create(
        obj_in=NetworkServiceCreateExtended(**item),
        region=db_region_with_single_project,
        projects=db_provider.projects,
    )


db_network_service = fixture_union(
    "db_network_service",
    (
        db_network_service_simple,
        db_network_service_with_networks,
        db_network_service_with_quotas,
    ),
    idstyle="explicit",
)
