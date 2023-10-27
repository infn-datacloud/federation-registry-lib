import subprocess
from typing import Dict, Generator

import pytest
from app.flavor.crud import flavor
from app.flavor.models import Flavor
from app.identity_provider.crud import identity_provider
from app.identity_provider.models import IdentityProvider
from app.image.crud import image
from app.location.crud import location
from app.location.models import Location
from app.main import app
from app.network.crud import network
from app.project.crud import project
from app.project.models import Project
from app.provider.crud import provider
from app.provider.models import Provider
from app.quota.crud import block_storage_quota, compute_quota
from app.quota.models import BlockStorageQuota, ComputeQuota
from app.region.crud import region
from app.region.models import Region
from app.service.crud import (
    block_storage_service,
    compute_service,
    identity_service,
    network_service,
)
from app.service.models import (
    BlockStorageService,
    ComputeService,
    IdentityService,
    NetworkService,
)
from app.sla.models import SLA
from app.user_group.models import UserGroup
from fastapi.testclient import TestClient
from neomodel import clear_neo4j_database, db
from tests.utils.block_storage_quota import create_random_block_storage_quota
from tests.utils.block_storage_service import create_random_block_storage_service
from tests.utils.compute_quota import create_random_compute_quota
from tests.utils.compute_service import create_random_compute_service
from tests.utils.flavor import create_random_flavor
from tests.utils.identity_provider import create_random_identity_provider
from tests.utils.identity_service import create_random_identity_service
from tests.utils.image import create_random_image
from tests.utils.location import create_random_location
from tests.utils.network import create_random_network
from tests.utils.network_service import create_random_network_service
from tests.utils.project import create_random_project
from tests.utils.provider import create_random_provider, random_type
from tests.utils.region import create_random_region

pytest.register_assert_rewrite("tests.utils")


@pytest.fixture
def setup_and_teardown_db() -> Generator:
    clear_neo4j_database(db)
    yield
    clear_neo4j_database(db)


# PROVIDERS


@pytest.fixture
def db_provider(setup_and_teardown_db: Generator) -> Provider:
    """First Provider with no relationships."""
    item_in = create_random_provider()
    item = provider.create(obj_in=item_in)
    yield item


@pytest.fixture
def db_provider2(db_provider: Provider) -> Provider:
    """Second Provider with no relationships.

    If the first is public, this is private. It has the same type as the
    first one.
    """
    item_in = create_random_provider()
    item_in.is_public = not db_provider.is_public
    item_in.type = db_provider.type
    item = provider.create(obj_in=item_in)
    yield item


@pytest.fixture
def db_provider3(db_provider2: Provider) -> Provider:
    """Third Provider with no relationships.

    It has a different type from the other two providers.
    """
    item_in = create_random_provider()
    while item_in.type == item_in.type:
        item_in.type = random_type()
    item = provider.create(obj_in=item_in)
    yield item


# PROJECTS (and related providers)


@pytest.fixture
def db_project(db_provider: Provider) -> Project:
    """Project owned by first provider."""
    item_in = create_random_project()
    db_project = project.create(obj_in=item_in, provider=db_provider)
    yield db_project


@pytest.fixture
def db_project2(db_provider2: Provider) -> Project:
    """First project owned by second provider."""
    item_in = create_random_project()
    db_project = project.create(obj_in=item_in, provider=db_provider2)
    yield db_project


@pytest.fixture
def db_project3(db_project2: Project) -> Project:
    """Second project owned by second provider."""
    item_in = create_random_project()
    db_project = project.create(obj_in=item_in, provider=db_project2.provider.single())
    yield db_project


@pytest.fixture
def db_provider_with_single_project(db_project: Project) -> Provider:
    """Provider with a single project."""
    yield db_project.provider.single()


@pytest.fixture
def db_provider_with_multiple_projects(db_project3: Project) -> Provider:
    """Provider with multiple (2) projects."""
    yield db_project3.provider.single()


# IDENTITY PROVIDERS (and related providers)


@pytest.fixture
def db_idp_with_single_user_group(
    db_provider_with_single_project: Provider,
) -> IdentityProvider:
    """Identity Provider with a single user group.

    It is linked to the provider with only one project.
    """
    item_in = create_random_identity_provider(
        projects=[i.uuid for i in db_provider_with_single_project.projects]
    )
    item = identity_provider.create(
        obj_in=item_in, provider=db_provider_with_single_project
    )
    yield item


@pytest.fixture
def db_idp_with_multiple_user_groups(
    db_provider_with_multiple_projects: Provider,
) -> IdentityProvider:
    """Identity Provider with multiple user groups.

    It is linked to the provider with multiple projects and generates a
    user group for each provider project.
    """
    item_in = create_random_identity_provider(
        projects=[i.uuid for i in db_provider_with_multiple_projects.projects]
    )
    item = identity_provider.create(
        obj_in=item_in, provider=db_provider_with_multiple_projects
    )
    yield item


@pytest.fixture
def db_idp_with_multiple_providers(
    db_provider_with_single_project: Provider,
    db_provider_with_multiple_projects: Provider,
) -> IdentityProvider:
    """Identity Provider with multiple user groups, linked to multiple
    providers.

    It has a user group on a provider and 2 user groups on the other
    one. Each user group points to exactly one project.
    """
    item_in = create_random_identity_provider(
        projects=[i.uuid for i in db_provider_with_single_project.projects]
    )
    item = identity_provider.create(
        obj_in=item_in, provider=db_provider_with_single_project
    )
    item_in.user_groups = create_random_identity_provider(
        projects=[i.uuid for i in db_provider_with_multiple_projects.projects]
    ).user_groups
    item = identity_provider.create(
        obj_in=item_in, provider=db_provider_with_multiple_projects
    )
    yield item


@pytest.fixture
def db_provider_with_single_idp(
    db_idp_with_single_user_group: IdentityProvider,
) -> Provider:
    """Provider with a single authorized IDP and a single project."""
    return db_idp_with_single_user_group.providers.all()[0]


@pytest.fixture
def db_provider_with_multiple_idps(
    db_provider_with_multiple_projects: Provider,
) -> Provider:
    """Provider with a multiple authorized IDP and multiple projects.

    Each IDP has a single user group. Each user group points to a
    different project.
    """
    db_project1 = db_provider_with_multiple_projects.projects.all()[0]
    db_project2 = db_provider_with_multiple_projects.projects.all()[1]
    item_in = create_random_identity_provider(projects=[db_project1.uuid])
    identity_provider.create(
        obj_in=item_in, provider=db_provider_with_multiple_projects
    )
    item_in = create_random_identity_provider(projects=[db_project2.uuid])
    identity_provider.create(
        obj_in=item_in, provider=db_provider_with_multiple_projects
    )
    yield db_provider_with_multiple_projects


# USER GROUPS


@pytest.fixture
def db_user_group(db_idp_with_single_user_group: IdentityProvider) -> UserGroup:
    """User group owned by the idp with just one user group.

    It has just one SLA.
    """
    yield db_idp_with_single_user_group.user_groups.all()[0]


@pytest.fixture
def db_user_group2(db_idp_with_multiple_user_groups: IdentityProvider) -> UserGroup:
    """First user group owned by the idp with multiple user groups.

    It has just one SLA.
    """
    yield db_idp_with_multiple_user_groups.user_groups.all()[0]


@pytest.fixture
def db_user_group3(db_idp_with_multiple_user_groups: IdentityProvider) -> UserGroup:
    """Second user group owned by the idp with multiple user groups.

    It has just one SLA.
    """
    yield db_idp_with_multiple_user_groups.user_groups.all()[1]


@pytest.fixture
def db_user_group_with_multiple_slas(
    db_provider_with_single_project: Provider,
    db_provider_with_multiple_projects: Provider,
) -> IdentityProvider:
    """User Group with multiple SLAs.

    Each SLA points to a project belonging to a different provider.
    """
    item_in = create_random_identity_provider(
        projects=[i.uuid for i in db_provider_with_single_project.projects]
    )
    item = identity_provider.create(
        obj_in=item_in, provider=db_provider_with_single_project
    )
    item_in.user_groups[0].sla = (
        create_random_identity_provider(
            projects=[i.uuid for i in db_provider_with_multiple_projects.projects]
        )
        .user_groups[0]
        .sla
    )
    item = identity_provider.create(
        obj_in=item_in, provider=db_provider_with_multiple_projects
    )
    yield item.user_groups.all()[0]


# SLAS


@pytest.fixture
def db_sla(db_user_group: UserGroup) -> SLA:
    """SLA owned by the user group of the provider with just one project."""
    yield db_user_group.slas.all()[0]


@pytest.fixture
def db_sla2(db_user_group2: UserGroup) -> SLA:
    """SLA owned by first user group of the provider with multiple projects."""
    yield db_user_group2.slas.all()[0]


@pytest.fixture
def db_sla3(db_user_group3: UserGroup) -> SLA:
    """SLA owned by second user group of the provider with multiple
    projects."""
    yield db_user_group3.slas.all()[0]


# TODO Create SLA fixture with multiple projects of different providers


# REGIONS


@pytest.fixture
def db_region(db_provider: Provider) -> Region:
    """Region owned by first provider."""
    item_in = create_random_region()
    item = region.create(obj_in=item_in, provider=db_provider)
    yield item


@pytest.fixture
def db_region2(db_provider2: Provider) -> Region:
    """First region owned by second provider."""
    item_in = create_random_region()
    item = region.create(obj_in=item_in, provider=db_provider2)
    yield item


@pytest.fixture
def db_region3(db_region2: Region) -> Region:
    """Second region owned by second provider."""
    item_in = create_random_region()
    item = region.create(obj_in=item_in, provider=db_region2.provider.single())
    yield item


@pytest.fixture
def db_provider_with_single_region(db_region: Region) -> Region:
    """Provider with single region."""
    yield db_region.provider.single()


@pytest.fixture
def db_provider_with_multiple_regions(db_region3: Region) -> Region:
    """Provider with multiple regions."""
    yield db_region3.provider.single()


# LOCATIONS (and related regions)


@pytest.fixture
def db_location(db_region: Region) -> Location:
    item_in = create_random_location()
    item = location.create(obj_in=item_in, region=db_region)
    yield item


@pytest.fixture
def db_location_with_multiple_regions(db_region2: Region) -> Location:
    item_in = create_random_location()
    item = location.create(obj_in=item_in, region=db_region2)
    yield item


@pytest.fixture
def db_block_storage_serv(db_region: Region) -> ComputeService:
    item_in = create_random_block_storage_service()
    item = block_storage_service.create(obj_in=item_in, region=db_region)
    yield item


@pytest.fixture
def db_block_storage_serv2(db_region2: Region) -> ComputeService:
    item_in = create_random_block_storage_service()
    item = block_storage_service.create(obj_in=item_in, region=db_region2)
    yield item


@pytest.fixture
def db_block_storage_quota(
    db_block_storage_serv: BlockStorageService,
) -> BlockStorageQuota:
    db_region = db_block_storage_serv.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.all()[0]
    item_in = create_random_block_storage_quota(project=db_project.uuid)
    item_in.per_user = False
    item = block_storage_quota.create(
        obj_in=item_in, service=db_block_storage_serv, project=db_project
    )
    yield item


@pytest.fixture
def db_block_storage_quota_per_user(
    db_block_storage_serv: BlockStorageService,
) -> BlockStorageQuota:
    db_region = db_block_storage_serv.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.all()[0]
    item_in = create_random_block_storage_quota(project=db_project.uuid)
    item_in.per_user = True
    item = block_storage_quota.create(
        obj_in=item_in, service=db_block_storage_serv, project=db_project
    )
    yield item


@pytest.fixture
def db_compute_serv(db_region: Region) -> ComputeService:
    item_in = create_random_compute_service()
    item = compute_service.create(obj_in=item_in, region=db_region)
    yield item


@pytest.fixture
def db_compute_serv2(db_region2: Region) -> ComputeService:
    item_in = create_random_compute_service()
    item = compute_service.create(obj_in=item_in, region=db_region2)
    yield item


@pytest.fixture
def db_compute_quota(db_compute_serv: ComputeService) -> ComputeQuota:
    db_region = db_compute_serv.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.all()[0]
    item_in = create_random_compute_quota(project=db_project.uuid)
    item_in.per_user = False
    item = compute_quota.create(
        obj_in=item_in, service=db_compute_serv, project=db_project
    )
    yield item


@pytest.fixture
def db_compute_quota_per_user(db_compute_serv: ComputeService) -> ComputeQuota:
    db_region = db_compute_serv.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.all()[0]
    item_in = create_random_compute_quota(project=db_project.uuid)
    item_in.per_user = True
    item = compute_quota.create(
        obj_in=item_in, service=db_compute_serv, project=db_project
    )
    yield item


@pytest.fixture
def db_public_flavor(db_compute_serv: ComputeService) -> Flavor:
    item_in = create_random_flavor()
    item = flavor.create(obj_in=item_in, service=db_compute_serv)
    yield item


@pytest.fixture
def db_private_flavor(db_compute_serv: ComputeService) -> Flavor:
    db_region = db_compute_serv.region.single()
    db_provider = db_region.provider.single()
    item_in = create_random_flavor(projects=[i.uuid for i in db_provider.projects])
    item = flavor.create(
        obj_in=item_in, service=db_compute_serv, projects=db_provider.projects
    )
    yield item


@pytest.fixture
def db_public_image(db_compute_serv: ComputeService) -> Flavor:
    item_in = create_random_image()
    item = image.create(obj_in=item_in, service=db_compute_serv)
    yield item


@pytest.fixture
def db_private_image(db_compute_serv: ComputeService) -> Flavor:
    db_region = db_compute_serv.region.single()
    db_provider = db_region.provider.single()
    item_in = create_random_image(projects=[i.uuid for i in db_provider.projects])
    item = image.create(
        obj_in=item_in, service=db_compute_serv, projects=db_provider.projects
    )
    yield item


@pytest.fixture
def db_network_serv(db_region: Region) -> NetworkService:
    item_in = create_random_network_service()
    item = network_service.create(obj_in=item_in, region=db_region)
    yield item


@pytest.fixture
def db_network_serv2(db_region2: Region) -> NetworkService:
    item_in = create_random_network_service()
    item = network_service.create(obj_in=item_in, region=db_region2)
    yield item


@pytest.fixture
def db_public_network(db_network_serv: NetworkService) -> Flavor:
    item_in = create_random_network()
    item = network.create(obj_in=item_in, service=db_network_serv)
    yield item


@pytest.fixture
def db_private_network(db_network_serv: NetworkService) -> Flavor:
    db_region = db_network_serv.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.all()[0]
    item_in = create_random_network(project=db_project.uuid)
    item = network.create(obj_in=item_in, service=db_network_serv, project=db_project)
    yield item


@pytest.fixture
def db_identity_serv(db_region: Region) -> IdentityService:
    item_in = create_random_identity_service()
    item = identity_service.create(obj_in=item_in, region=db_region)
    yield item


@pytest.fixture
def db_identity_serv2(db_region2: Region) -> IdentityService:
    item_in = create_random_identity_service()
    item = identity_service.create(obj_in=item_in, region=db_region2)
    yield item


@pytest.fixture
def client(setup_and_teardown_db: Generator) -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture
def token() -> str:
    issuer = "https://iam.cloud.infn.it/"
    token_cmd = subprocess.run(
        [
            "docker",
            "exec",
            "catalog-api-oidc-agent-1",
            "oidc-token",
            issuer,
        ],
        stdout=subprocess.PIPE,
        text=True,
    )
    yield token_cmd.stdout.strip("\n")


@pytest.fixture
def read_header(token: str) -> Dict:
    return {"authorization": f"Bearer {token}"}


@pytest.fixture
def write_header(read_header: Dict) -> Dict:
    return {
        **read_header,
        "accept": "application/json",
        "content-type": "application/json",
    }
