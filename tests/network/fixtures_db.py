"""Network specific fixtures."""
from typing import Any, Dict

from pytest_cases import fixture, parametrize

from app.network.crud import network_mng
from app.network.models import Network
from app.project.models import Project
from app.provider.models import Provider
from app.provider.schemas_extended import NetworkCreateExtended
from app.region.models import Region
from app.service.models import NetworkService

is_shared = [True, False]


@fixture
@parametrize(is_shared=is_shared)
def db_network(
    is_shared: bool,
    network_create_mandatory_data: Dict[str, Any],
    db_network_service_with_single_project: NetworkService,
) -> Network:
    """Fixture with standard DB Network.

    The network can be public or private based on the number of allowed projects.
    0 - Public. 1 or 2 - Private.
    """
    db_region: Region = db_network_service_with_single_project.region.single()
    db_provider: Provider = db_region.provider.single()
    if is_shared:
        project = None
        db_project = None
    else:
        db_project: Project = db_provider.projects.single()
        project = db_project.uuid
    item = NetworkCreateExtended(
        **network_create_mandatory_data, is_shared=is_shared, project=project
    )
    return network_mng.create(
        obj_in=item,
        service=db_network_service_with_single_project,
        project=db_project,
    )
