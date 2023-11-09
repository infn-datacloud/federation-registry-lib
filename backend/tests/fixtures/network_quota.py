import pytest

from app.project.models import Project
from app.quota.crud import network_quota
from app.quota.models import NetworkQuota
from app.service.models import NetworkService
from tests.utils.network_quota import create_random_network_quota


@pytest.fixture
def db_network_quota(db_network_serv2: NetworkService) -> NetworkQuota:
    """Network Quota.

    It belongs to the Network Service belonging to the first region of the provider with
    multiple projects.

    Quota points to the first project. Quota to apply to the whole user group.
    """
    db_region = db_network_serv2.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.single()
    item_in = create_random_network_quota(project=db_project.uuid)
    item_in.per_user = False
    item = network_quota.create(
        obj_in=item_in, service=db_network_serv2, project=db_project
    )
    yield item


@pytest.fixture
def db_network_quota_per_user(db_network_quota: NetworkQuota) -> NetworkQuota:
    """Network Quota.

    It belongs to the Network Service belonging to the first region of the provider with
    multiple projects.

    Quota points to the first project. Quota to apply to each user of the user group.
    This is currently the second quota on the same project and same service.
    """
    db_service = db_network_quota.service.single()
    db_region = db_service.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.single()
    item_in = create_random_network_quota(project=db_project.uuid)
    item_in.per_user = True
    item = network_quota.create(obj_in=item_in, service=db_service, project=db_project)
    yield item


@pytest.fixture
def db_network_quota2(db_network_quota_per_user: NetworkQuota) -> NetworkQuota:
    """Network Quota.

    It belongs to the Network Service belonging to the first region of the provider with
    multiple projects.

    Quota points to the second project. Quota to apply to the whole user group. This is
    the third quota on the same service.
    """
    db_service = db_network_quota_per_user.service.single()
    db_region = db_service.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.all()[1]
    item_in = create_random_network_quota(project=db_project.uuid)
    item_in.per_user = False
    item = network_quota.create(obj_in=item_in, service=db_service, project=db_project)
    yield item


@pytest.fixture
def db_network_quota3(
    db_network_quota2: NetworkQuota, db_network_serv3: NetworkService
) -> NetworkQuota:
    """Network Quota.

    It belongs to the Network Service belonging to the second region of the provider
    with a multiple projects.

    Quota points to the second project. Quota to apply to the whole user group.
    """
    db_region = db_network_serv3.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.all()[1]
    item_in = create_random_network_quota(project=db_project.uuid)
    item_in.per_user = False
    item = network_quota.create(
        obj_in=item_in, service=db_network_serv3, project=db_project
    )
    yield item


@pytest.fixture
def db_network_serv_with_single_quota(db_network_quota: NetworkQuota) -> NetworkService:
    """Project with single Network Quota."""
    yield db_network_quota.service.single()


@pytest.fixture
def db_network_serv_with_multiple_quotas_same_project(
    db_network_quota_per_user: NetworkQuota
) -> NetworkService:
    """Project with multiple Network Quota on same project."""
    yield db_network_quota_per_user.service.single()


@pytest.fixture
def db_network_serv_with_multiple_quotas(
    db_network_quota2: NetworkQuota
) -> NetworkService:
    """Project with single Network Quota."""
    yield db_network_quota2.service.single()


@pytest.fixture
def db_project_with_single_network_quota(db_network_quota: NetworkQuota) -> Project:
    """Project with single Network Quota."""
    yield db_network_quota.project.single()


@pytest.fixture
def db_project_with_multiple_network_quotas_same_service(
    db_network_quota_per_user: NetworkQuota
) -> Project:
    """Project with multiple Network Quotas on same service."""
    yield db_network_quota_per_user.project.single()


@pytest.fixture
def db_project_with_multiple_network_quotas_diff_service(
    db_network_quota3: NetworkQuota
) -> Project:
    """Project with multiple Network Quotas on different services."""
    yield db_network_quota3.project.single()
