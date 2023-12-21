"""NetworkQuota specific fixtures."""
from pytest_cases import fixture

from app.project.models import Project
from app.provider.models import Provider
from app.provider.schemas_extended import NetworkQuotaCreateExtended
from app.quota.crud import network_quota_mng
from app.quota.models import NetworkQuota
from app.region.models import Region
from app.service.models import NetworkService
from tests.quotas.network_quota.utils import random_network_quota_required_attr


@fixture
def db_network_quota(
    db_network_service_with_single_project: NetworkService,
) -> NetworkQuota:
    """Fixture with standard DB NetworkQuota."""
    db_region: Region = db_network_service_with_single_project.region.single()
    db_provider: Provider = db_region.provider.single()
    db_project: Project = db_provider.projects.single()
    item = {**random_network_quota_required_attr(), "project": db_project.uuid}
    return network_quota_mng.create(
        obj_in=NetworkQuotaCreateExtended(**item),
        service=db_network_service_with_single_project,
        project=db_project,
    )
