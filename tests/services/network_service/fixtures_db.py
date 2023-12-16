"""NetworkService specific fixtures."""
from typing import Any, Dict
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
from tests.utils.utils import random_lower_string

relationships_num = [1, 2]


@fixture
def db_network_service_simple(
    network_service_create_mandatory_data: Dict[str, Any], db_region_simple: Region
) -> NetworkService:
    """Fixture with standard DB NetworkService."""
    item = NetworkServiceCreateExtended(**network_service_create_mandatory_data)
    return network_service_mng.create(obj_in=item, region=db_region_simple)


@fixture
def db_network_service_with_single_project(
    network_service_create_mandatory_data: Dict[str, Any],
    db_region_with_single_project: Region,
) -> NetworkService:
    """Fixture with standard DB NetworkService."""
    item = NetworkServiceCreateExtended(**network_service_create_mandatory_data)
    return network_service_mng.create(obj_in=item, region=db_region_with_single_project)


@fixture
@parametrize(owned_quotas=relationships_num)
def db_network_service_with_quotas(
    owned_quotas: int,
    network_service_create_mandatory_data: Dict[str, Any],
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
        **network_service_create_mandatory_data, quotas=quotas
    )
    return network_service_mng.create(
        obj_in=item, region=db_region_with_projects, projects=db_provider.projects
    )


@fixture
@parametrize(owned_networks=relationships_num)
def db_network_service_with_networks(
    owned_networks: int,
    network_service_create_mandatory_data: Dict[str, Any],
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
        **network_service_create_mandatory_data, networks=networks
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
