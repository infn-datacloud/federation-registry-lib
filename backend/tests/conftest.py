import subprocess
from typing import Dict, Generator

import pytest
from app.flavor.crud import flavor
from app.flavor.models import Flavor
from app.identity_provider.crud import identity_provider
from app.identity_provider.models import IdentityProvider
from app.image.crud import image
from app.image.models import Image
from app.location.crud import location
from app.location.models import Location
from app.main import app
from app.network.crud import network
from app.network.models import Network
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


# DB specific fixtures


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
) -> UserGroup:
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


# REGIONS (and related providers)


@pytest.fixture
def db_region(db_provider_with_single_project: Provider) -> Region:
    """Region owned by provider with a single project."""
    item_in = create_random_region()
    item = region.create(obj_in=item_in, provider=db_provider_with_single_project)
    yield item


@pytest.fixture
def db_region2(db_provider_with_multiple_projects: Provider) -> Region:
    """First region owned by the provider with multiple regions."""
    item_in = create_random_region()
    item = region.create(obj_in=item_in, provider=db_provider_with_multiple_projects)
    yield item


@pytest.fixture
def db_region3(db_region2: Region) -> Region:
    """Second region owned by the provider with multiple regions."""
    item_in = create_random_region()
    item = region.create(obj_in=item_in, provider=db_region2.provider.single())
    yield item


@pytest.fixture
def db_provider_with_single_region(db_region: Region) -> Provider:
    """Provider with single region."""
    yield db_region.provider.single()


@pytest.fixture
def db_provider_with_multiple_regions(db_region3: Region) -> Provider:
    """Provider with multiple regions."""
    yield db_region3.provider.single()


# LOCATIONS (and related regions)


@pytest.fixture
def db_location(db_region: Region) -> Location:
    """Location of the region of the first provider."""
    item_in = create_random_location()
    item = location.create(obj_in=item_in, region=db_region)
    yield item


@pytest.fixture
def db_location2(db_region2: Region) -> Location:
    """Location of the first region of the second provider."""
    item_in = create_random_location()
    item = location.create(obj_in=item_in, region=db_region2)
    yield item


@pytest.fixture
def db_location_with_multiple_regions(
    db_location: Location, db_region3: Region
) -> Location:
    """Location connected to the region of the first provider and the second
    region of the second provider."""
    item_in = create_random_location()
    item_in.site = db_location.site
    item = location.create(obj_in=item_in, region=db_region3)
    yield item


@pytest.fixture
def db_region_with_location(db_location: Location) -> Region:
    """Region with a location."""
    yield db_location.regions.all()[0]


# BLOCK STORAGE SERVICES (and related regions)


@pytest.fixture
def db_block_storage_serv(db_region: Region) -> BlockStorageService:
    """Block Storage service on the region of the first provider."""
    item_in = create_random_block_storage_service()
    item = block_storage_service.create(obj_in=item_in, region=db_region)
    yield item


@pytest.fixture
def db_block_storage_serv2(db_region2: Region) -> BlockStorageService:
    """Block Storage service on the first region of the second provider."""
    item_in = create_random_block_storage_service()
    item = block_storage_service.create(obj_in=item_in, region=db_region2)
    yield item


@pytest.fixture
def db_block_storage_serv3(db_region3: Region) -> BlockStorageService:
    """Block Storage service on the second region of the second provider."""
    item_in = create_random_block_storage_service()
    item = block_storage_service.create(obj_in=item_in, region=db_region3)
    yield item


# TODO Add fixture of second block_storage_service for the same region?


@pytest.fixture
def db_region_with_block_storage_service(
    db_block_storage_serv: BlockStorageService,
) -> Region:
    """Region with a block storage service."""
    yield db_block_storage_serv.region.single()


# TODO Add fixture of region with multiple block_storage_services?


# BLOCK STORAGE QUOTA (and related projects and services)


@pytest.fixture
def db_block_storage_quota(
    db_block_storage_serv2: BlockStorageService,
) -> BlockStorageQuota:
    """Block Storage Quota of the BS Service belonging to the first region of
    the provider with multiple projects.

    Quota points to the first project. Quota to apply to the whole user
    group.
    """
    db_region = db_block_storage_serv2.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.all()[0]
    item_in = create_random_block_storage_quota(project=db_project.uuid)
    item_in.per_user = False
    item = block_storage_quota.create(
        obj_in=item_in, service=db_block_storage_serv2, project=db_project
    )
    yield item


@pytest.fixture
def db_block_storage_quota_per_user(
    db_block_storage_quota: BlockStorageQuota,
) -> BlockStorageQuota:
    """Block Storage Quota of the BS Service belonging to the first region of
    the provider with multiple projects.

    Quota points to the first project. Quota to apply to each user of
    the user group. This is currently the second quota on the same
    project and same service.
    """
    db_service = db_block_storage_quota.service.single()
    db_region = db_service.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.all()[0]
    item_in = create_random_block_storage_quota(project=db_project.uuid)
    item_in.per_user = True
    item = block_storage_quota.create(
        obj_in=item_in, service=db_service, project=db_project
    )
    yield item


@pytest.fixture
def db_block_storage_quota2(
    db_block_storage_quota_per_user: BlockStorageQuota,
) -> BlockStorageQuota:
    """Block Storage Quota of the BS Service belonging to the first region of
    the provider with multiple projects.

    Quota points to the second project. Quota to apply to the whole user
    group. This is the third quota on the same service.
    """
    db_service = db_block_storage_quota_per_user.service.single()
    db_region = db_service.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.all()[1]
    item_in = create_random_block_storage_quota(project=db_project.uuid)
    item_in.per_user = False
    item = block_storage_quota.create(
        obj_in=item_in, service=db_service, project=db_project
    )
    yield item


@pytest.fixture
def db_block_storage_quota3(
    db_block_storage_quota2: BlockStorageQuota,
    db_block_storage_serv3: BlockStorageService,
) -> BlockStorageQuota:
    """Block Storage Quota of the BS Service belonging to the second region of
    the provider with a multiple projects.

    Quota points to the second project. Quota to apply to the whole user
    group.
    """
    db_region = db_block_storage_serv3.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.all()[1]
    item_in = create_random_block_storage_quota(project=db_project.uuid)
    item_in.per_user = False
    item = block_storage_quota.create(
        obj_in=item_in, service=db_block_storage_serv3, project=db_project
    )
    yield item


@pytest.fixture
def db_block_storage_serv_with_single_quota(
    db_block_storage_quota: BlockStorageQuota,
) -> BlockStorageService:
    """Project with single Block Storage Quota."""
    yield db_block_storage_quota.service.all()[0]


@pytest.fixture
def db_block_storage_serv_with_multiple_quotas(
    db_block_storage_quota2: BlockStorageQuota,
) -> BlockStorageService:
    """Project with single Block Storage Quota."""
    yield db_block_storage_quota2.service.all()[0]


@pytest.fixture
def db_project_with_single_block_storage_quota(
    db_block_storage_quota: BlockStorageQuota,
) -> Project:
    """Project with single Block Storage Quota."""
    yield db_block_storage_quota.project.single()


@pytest.fixture
def db_project_with_multiple_block_storage_quotas_same_service(
    db_block_storage_quota_per_user: BlockStorageQuota,
) -> Project:
    """Project with multiple Block Storage Quotas on same service."""
    yield db_block_storage_quota_per_user.project.single()


@pytest.fixture
def db_project_with_multiple_block_storage_quotas_diff_service(
    db_block_storage_quota3: BlockStorageQuota,
) -> Project:
    """Project with single Block Storage Quota."""
    yield db_block_storage_quota3.project.single()


# COMPUTE SERVICES (and related regions)


@pytest.fixture
def db_compute_serv(db_region: Region) -> ComputeService:
    """Compute service on the region of the first provider."""
    item_in = create_random_compute_service()
    item = compute_service.create(obj_in=item_in, region=db_region)
    yield item


@pytest.fixture
def db_compute_serv2(db_region2: Region) -> ComputeService:
    """Compute service on first region of the second provider."""
    item_in = create_random_compute_service()
    item = compute_service.create(obj_in=item_in, region=db_region2)
    yield item


@pytest.fixture
def db_compute_serv3(db_region3: Region) -> ComputeService:
    """Compute service on the second region of the second provider."""
    item_in = create_random_compute_service()
    item = compute_service.create(obj_in=item_in, region=db_region3)
    yield item


# TODO Add fixture of second compute_service for the same region?


@pytest.fixture
def db_region_with_compute_service(db_compute_serv: ComputeService) -> Region:
    """Region with a block storage service."""
    yield db_compute_serv.region.single()


# TODO Add fixture of region with multiple compute_services?


# COMPUTE QUOTA (and related projects and services)


@pytest.fixture
def db_compute_quota(
    db_compute_serv2: BlockStorageService,
) -> BlockStorageQuota:
    """Compute Quota of the C Service belonging to the first region of the
    provider with multiple projects.

    Quota points to the first project. Quota to apply to the whole user
    group.
    """
    db_region = db_compute_serv2.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.all()[0]
    item_in = create_random_compute_quota(project=db_project.uuid)
    item_in.per_user = False
    item = compute_quota.create(
        obj_in=item_in, service=db_compute_serv2, project=db_project
    )
    yield item


@pytest.fixture
def db_compute_quota_per_user(
    db_compute_quota: ComputeQuota,
) -> ComputeQuota:
    """Compute Quota of the C Service belonging to the first region of the
    provider with multiple projects.

    Quota points to the first project. Quota to apply to each user of
    the user group. This is currently the second quota on the same
    project and same service.
    """
    db_service = db_compute_quota.service.single()
    db_region = db_service.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.all()[0]
    item_in = create_random_compute_quota(project=db_project.uuid)
    item_in.per_user = True
    item = compute_quota.create(obj_in=item_in, service=db_service, project=db_project)
    yield item


@pytest.fixture
def db_compute_quota2(
    db_compute_quota_per_user: ComputeQuota,
) -> ComputeQuota:
    """Compute Quota of the C Service belonging to the first region of the
    provider with multiple projects.

    Quota points to the second project. Quota to apply to the whole user
    group. This is the third quota on the same service.
    """
    db_service = db_compute_quota_per_user.service.single()
    db_region = db_service.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.all()[1]
    item_in = create_random_compute_quota(project=db_project.uuid)
    item_in.per_user = False
    item = compute_quota.create(obj_in=item_in, service=db_service, project=db_project)
    yield item


@pytest.fixture
def db_compute_quota3(
    db_compute_quota2: ComputeQuota,
    db_compute_serv3: ComputeService,
) -> ComputeQuota:
    """Compute Quota of the C Service belonging to the second region of the
    provider with a multiple projects.

    Quota points to the second project. Quota to apply to the whole user
    group.
    """
    db_region = db_compute_serv3.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.all()[1]
    item_in = create_random_compute_quota(project=db_project.uuid)
    item_in.per_user = False
    item = compute_quota.create(
        obj_in=item_in, service=db_compute_serv3, project=db_project
    )
    yield item


@pytest.fixture
def db_compute_serv_with_single_quota(
    db_compute_quota: ComputeQuota,
) -> ComputeService:
    """Project with single Compute Quota."""
    yield db_compute_quota.service.all()[0]


@pytest.fixture
def db_compute_serv_with_multiple_quotas(
    db_compute_quota2: ComputeQuota,
) -> ComputeService:
    """Project with single Compute Quota."""
    yield db_compute_quota2.service.all()[0]


@pytest.fixture
def db_project_with_single_compute_quota(
    db_compute_quota: ComputeQuota,
) -> Project:
    """Project with single Compute Quota."""
    yield db_compute_quota.project.single()


@pytest.fixture
def db_project_with_multiple_compute_quotas_same_service(
    db_compute_quota_per_user: ComputeQuota,
) -> Project:
    """Project with multiple Compute Quotas on same service."""
    yield db_compute_quota_per_user.project.single()


@pytest.fixture
def db_project_with_multiple_compute_quotas_diff_service(
    db_compute_quota3: ComputeQuota,
) -> Project:
    """Project with multiple Compute Quotas on different services."""
    yield db_compute_quota3.project.single()


# FLAVORS (and related services and projects)


@pytest.fixture
def db_public_flavor(db_compute_serv2: ComputeService) -> Flavor:
    """Public flavor of a compute service."""
    item_in = create_random_flavor()
    item = flavor.create(obj_in=item_in, service=db_compute_serv2)
    yield item


@pytest.fixture
def db_private_flavor(db_public_flavor: Flavor) -> Flavor:
    """First private flavor of a compute service.

    It belongs to a specific project. It's the second flavor on the same
    service.
    """
    db_service = db_public_flavor.services.all()[0]
    db_region = db_service.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.all()[0]
    item_in = create_random_flavor(projects=[db_project.uuid])
    item = flavor.create(
        obj_in=item_in, service=db_service, projects=db_provider.projects
    )
    yield item


@pytest.fixture
def db_private_flavor_multiple_projects(db_public_flavor: Flavor) -> Flavor:
    """First private flavor of a compute service.

    It belongs to a all projects. It's the second flavor on the same
    service.
    """
    db_service = db_public_flavor.services.all()[0]
    db_region = db_service.region.single()
    db_provider = db_region.provider.single()
    item_in = create_random_flavor(projects=[i.uuid for i in db_provider.projects])
    item = flavor.create(
        obj_in=item_in, service=db_service, projects=db_provider.projects
    )
    yield item


@pytest.fixture
def db_private_flavor2(db_private_flavor: Flavor) -> Flavor:
    """Second private flavor of a compute service.

    It belongs to a specific project. It's the third flavor on the same
    service.
    """
    db_service = db_private_flavor.services.all()[0]
    db_region = db_service.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.all()[0]
    item_in = create_random_flavor(projects=[db_project.uuid])
    item = flavor.create(
        obj_in=item_in, service=db_service, projects=db_provider.projects
    )
    yield item


@pytest.fixture
def db_private_flavor3(
    db_private_flavor2: Flavor, db_compute_serv3: ComputeService
) -> Flavor:
    """First private flavor of another compute service.

    It belongs to a specific project. It's the first flavor on a
    different service.
    """
    db_region = db_compute_serv3.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.all()[0]
    item_in = create_random_flavor(projects=[db_project.uuid])
    item = flavor.create(
        obj_in=item_in, service=db_compute_serv3, projects=db_provider.projects
    )
    yield item


@pytest.fixture
def db_shared_flavor(db_compute_serv2: ComputeService, db_compute_serv3) -> Flavor:
    """Public flavor shared between different compute services of the same
    provider."""
    item_in = create_random_flavor()
    item = flavor.create(obj_in=item_in, service=db_compute_serv2)
    item = flavor.create(obj_in=item_in, service=db_compute_serv3)
    yield item


@pytest.fixture
def db_compute_serv_with_single_flavor(db_public_flavor: Flavor) -> ComputeService:
    """Project with single Flavor."""
    yield db_public_flavor.services.all()[0]


@pytest.fixture
def db_compute_serv_with_multiple_flavors(db_private_flavor: Flavor) -> ComputeService:
    """Project with multiple Flavors (public and private ones)."""
    yield db_private_flavor.services.all()[0]


@pytest.fixture
def db_project_with_single_private_flavor(db_private_flavor: Flavor) -> Project:
    """Project with single private Flavor."""
    yield db_private_flavor.projects.all()[0]


@pytest.fixture
def db_project_with_multiple_private_flavors_same_service(
    db_private_flavor2: Flavor,
) -> Project:
    """Project with multiple Flavors on same service."""
    yield db_private_flavor2.projects.all()[0]


@pytest.fixture
def db_project_with_multiple_private_flavors_diff_service(
    db_private_flavor3: Flavor,
) -> Project:
    """Project with multiple Flavors on different services."""
    yield db_private_flavor3.projects.all()[0]


# IMAGES (and related services and projects)


@pytest.fixture
def db_public_image(db_compute_serv2: ComputeService) -> Image:
    """Public image of a compute service."""
    item_in = create_random_image()
    item = image.create(obj_in=item_in, service=db_compute_serv2)
    yield item


@pytest.fixture
def db_private_image(db_public_image: Image) -> Image:
    """First private image of a compute service.

    It belongs to a specific project. It's the second image on the same
    service.
    """
    db_service = db_public_image.services.all()[0]
    db_region = db_service.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.all()[0]
    item_in = create_random_image(projects=[db_project.uuid])
    item = image.create(
        obj_in=item_in, service=db_service, projects=db_provider.projects
    )
    yield item


@pytest.fixture
def db_private_image_multiple_projects(db_public_image: Image) -> Image:
    """First private image of a compute service.

    It belongs to a all projects. It's the second image on the same
    service.
    """
    db_service = db_public_image.services.all()[0]
    db_region = db_service.region.single()
    db_provider = db_region.provider.single()
    item_in = create_random_image(projects=[i.uuid for i in db_provider.projects])
    item = image.create(
        obj_in=item_in, service=db_service, projects=db_provider.projects
    )
    yield item


@pytest.fixture
def db_private_image2(db_private_image: Image) -> Image:
    """Second private image of a compute service.

    It belongs to a specific project. It's the third image on the same
    service.
    """
    db_service = db_private_image.services.all()[0]
    db_region = db_service.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.all()[0]
    item_in = create_random_image(projects=[db_project.uuid])
    item = image.create(
        obj_in=item_in, service=db_service, projects=db_provider.projects
    )
    yield item


@pytest.fixture
def db_private_image3(
    db_private_image2: Image, db_compute_serv3: ComputeService
) -> Image:
    """First private image of another compute service.

    It belongs to a specific project. It's the first image on a
    different service.
    """
    db_region = db_compute_serv3.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.all()[0]
    item_in = create_random_image(projects=[db_project.uuid])
    item = image.create(
        obj_in=item_in, service=db_compute_serv3, projects=db_provider.projects
    )
    yield item


@pytest.fixture
def db_shared_image(db_compute_serv2: ComputeService, db_compute_serv3) -> Flavor:
    """Public image shared between different compute services of the same
    provider."""
    item_in = create_random_image()
    item = image.create(obj_in=item_in, service=db_compute_serv2)
    item = image.create(obj_in=item_in, service=db_compute_serv3)
    yield item


@pytest.fixture
def db_compute_serv_with_single_image(db_public_image: Image) -> ComputeService:
    """Project with single Image."""
    yield db_public_image.services.all()[0]


@pytest.fixture
def db_compute_serv_with_multiple_images(db_private_image: Image) -> ComputeService:
    """Project with multiple Images (public and private ones)."""
    yield db_private_image.services.all()[0]


@pytest.fixture
def db_project_with_single_private_image(db_private_image: Image) -> Project:
    """Project with single private Image."""
    yield db_private_image.projects.all()[0]


@pytest.fixture
def db_project_with_multiple_private_images_same_service(
    db_private_image2: Image,
) -> Project:
    """Project with multiple Images on same service."""
    yield db_private_image2.projects.all()[0]


@pytest.fixture
def db_project_with_multiple_private_images_diff_service(
    db_private_image3: Image,
) -> Project:
    """Project with multiple Images on different services."""
    yield db_private_image3.projects.all()[0]


# NETWORK SERVICES (and related regions)


@pytest.fixture
def db_network_serv(db_region: Region) -> NetworkService:
    """Network service on the region of the first provider."""
    item_in = create_random_network_service()
    item = network_service.create(obj_in=item_in, region=db_region)
    yield item


@pytest.fixture
def db_network_serv2(db_region2: Region) -> NetworkService:
    """Network service on first region of the second provider."""
    item_in = create_random_network_service()
    item = network_service.create(obj_in=item_in, region=db_region2)
    yield item


@pytest.fixture
def db_network_serv3(db_region3: Region) -> NetworkService:
    """Network service on the second region of the second provider."""
    item_in = create_random_network_service()
    item = network_service.create(obj_in=item_in, region=db_region3)
    yield item


# TODO Add fixture of second network_service for the same region?


@pytest.fixture
def db_region_with_network_service(db_network_serv: NetworkService) -> Region:
    """Region with a block storage service."""
    yield db_network_serv.region.single()


# TODO Add fixture of region with multiple network_services?


# NETWORKS (and related services and projects)


@pytest.fixture
def db_public_network(db_network_serv2: NetworkService) -> Network:
    """Public network of a network service."""
    item_in = create_random_network()
    item = network.create(obj_in=item_in, service=db_network_serv2)
    yield item


@pytest.fixture
def db_private_network(db_public_network: Network) -> Network:
    """First private network of a network service.

    It belongs to a specific project. It's the second network on the
    same service.
    """
    db_service = db_public_network.service.single()
    db_region = db_service.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.all()[0]
    item_in = create_random_network(project=db_project.uuid)
    item = network.create(obj_in=item_in, service=db_service, project=db_project)
    yield item


@pytest.fixture
def db_private_network2(db_private_network: Network) -> Network:
    """Second private network of a network service.

    It belongs to a specific project. It's the third network on the same
    service.
    """
    db_service = db_private_network.service.single()
    db_region = db_service.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.all()[0]
    item_in = create_random_network(project=db_project.uuid)
    item = network.create(obj_in=item_in, service=db_service, project=db_project)
    yield item


@pytest.fixture
def db_private_network3(
    db_private_network2: Network, db_network_serv3: NetworkService
) -> Network:
    """First private network of another network service.

    It belongs to a specific project. It's the first network on a
    different service.
    """
    db_region = db_network_serv3.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.all()[0]
    item_in = create_random_network(project=db_project.uuid)
    item = network.create(obj_in=item_in, service=db_network_serv3, project=db_project)
    yield item


@pytest.fixture
def db_network_serv_with_single_network(db_public_network: Network) -> NetworkService:
    """Network service with single Network."""
    yield db_public_network.service.single()


@pytest.fixture
def db_network_serv_with_multiple_networks(
    db_private_network: Network,
) -> NetworkService:
    """Network service with multiple Networks (public and private ones)."""
    yield db_private_network.service.single()


@pytest.fixture
def db_project_with_single_private_network(db_private_network: Network) -> Project:
    """Project with single private Network."""
    yield db_private_network.project.single()


@pytest.fixture
def db_project_with_multiple_private_networks_same_service(
    db_private_network2: Network,
) -> Project:
    """Project with multiple Networks on same service."""
    yield db_private_network2.project.single()


@pytest.fixture
def db_project_with_multiple_private_networks_diff_service(
    db_private_network3: Network,
) -> Project:
    """Project with multiple Networks on different services."""
    yield db_private_network3.project.single()


# IDENTITY SERVICES (and related regions)


@pytest.fixture
def db_identity_serv(db_region: Region) -> IdentityService:
    """Identity service on the region of the first provider."""
    item_in = create_random_identity_service()
    item = identity_service.create(obj_in=item_in, region=db_region)
    yield item


@pytest.fixture
def db_identity_serv2(db_region2: Region) -> IdentityService:
    """Identity service on first region of the second provider."""
    item_in = create_random_identity_service()
    item = identity_service.create(obj_in=item_in, region=db_region2)
    yield item


@pytest.fixture
def db_region_with_identity_service(db_identity_serv: IdentityService) -> Region:
    """Region with a block storage service."""
    yield db_identity_serv.region.single()


# API specific fixtures


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
