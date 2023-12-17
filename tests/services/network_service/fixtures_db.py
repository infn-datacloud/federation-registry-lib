"""NetworkService specific fixtures."""
from uuid import uuid4

from pytest_cases import fixture, fixture_union, parametrize

from app.provider.models import Provider
from app.provider.schemas_extended import (
    NetworkCreateExtended,
    NetworkQuotaCreateExtended,
    NetworkServiceCreateExtended,
)
from app.region.models import Region
from app.service.crud import network_service_mng
from app.service.models import NetworkService
from tests.common.utils import random_lower_string
from tests.services.network_service.utils import random_network_service_required_attr

relationships_num = [1, 2]


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
@parametrize(owned_quotas=relationships_num)
def db_network_service_with_quotas(
    owned_quotas: int,
    db_region_with_projects: Region,
) -> NetworkService:
    """Fixture with standard DB NetworkService."""
    db_provider: Provider = db_region_with_projects.provider.single()
    projects = [i.uuid for i in db_provider.projects]
    quotas = []
    for i in projects:
        for n in range(owned_quotas):
            quotas.append(NetworkQuotaCreateExtended(per_user=n % 2, project=i))
    item = NetworkServiceCreateExtended(
        **random_network_service_required_attr(), quotas=quotas
    )
    return network_service_mng.create(
        obj_in=item, region=db_region_with_projects, projects=db_provider.projects
    )


@fixture
@parametrize(owned_networks=relationships_num)
def db_network_service_with_networks(
    owned_networks: int,
    db_region_with_projects: Region,
) -> NetworkService:
    """Fixture with standard DB NetworkService."""
    db_provider: Provider = db_region_with_projects.provider.single()
    projects = [i.uuid for i in db_provider.projects]
    networks = [NetworkCreateExtended(name=random_lower_string(), uuid=uuid4())]
    for i in projects:
        for _ in range(owned_networks):
            networks.append(
                NetworkCreateExtended(
                    name=random_lower_string(), uuid=uuid4(), is_shared=False, project=i
                )
            )
    item = NetworkServiceCreateExtended(
        **random_network_service_required_attr(), networks=networks
    )
    return network_service_mng.create(
        obj_in=item, region=db_region_with_projects, projects=db_provider.projects
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
