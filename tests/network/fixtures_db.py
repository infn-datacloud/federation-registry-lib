"""Network specific fixtures."""
from pytest_cases import fixture, fixture_union

from app.network.crud import network_mng
from app.network.models import Network
from app.project.models import Project
from app.provider.models import Provider
from app.provider.schemas_extended import NetworkCreateExtended
from app.region.models import Region
from app.service.models import NetworkService
from tests.network.utils import random_network_required_attr


@fixture
def db_network_shared(db_network_service_simple: NetworkService) -> Network:
    """Fixture with standard DB Network.

    The network can be public or private based on the number of allowed projects.
    0 - Public. 1 or 2 - Private.
    """
    item = random_network_required_attr()
    return network_mng.create(
        obj_in=NetworkCreateExtended(**item), service=db_network_service_simple
    )


@fixture
def db_network_private(
    db_network_service_with_single_project: NetworkService,
) -> Network:
    """Fixture with standard DB Network.

    The network can be public or private based on the number of allowed projects.
    0 - Public. 1 or 2 - Private.
    """
    db_region: Region = db_network_service_with_single_project.region.single()
    db_provider: Provider = db_region.provider.single()
    db_project: Project = db_provider.projects.single()
    item = {
        **random_network_required_attr(),
        "is_shared": False,
        "project": db_project.uuid,
    }
    return network_mng.create(
        obj_in=NetworkCreateExtended(**item),
        service=db_network_service_with_single_project,
        project=db_project,
    )


db_network = fixture_union(
    "db_network",
    (db_network_private, db_network_shared),
    idstyle="explicit",
)
