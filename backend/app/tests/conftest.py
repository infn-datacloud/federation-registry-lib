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
from app.provider.crud import provider
from app.provider.models import Provider
from app.quota.crud import block_storage_quota, compute_quota
from app.quota.models import BlockStorageQuota, ComputeQuota
from app.region.crud import region
from app.region.models import Region
from app.service.crud import block_storage_service, compute_service, network_service
from app.service.models import BlockStorageService, ComputeService, NetworkService
from app.sla.models import SLA
from app.tests.utils.flavor import create_random_flavor
from app.tests.utils.identity_provider import create_random_identity_provider
from app.tests.utils.image import create_random_image
from app.tests.utils.location import create_random_location
from app.tests.utils.network import create_random_network
from app.tests.utils.project import create_random_project
from app.tests.utils.provider import create_random_provider
from app.tests.utils.quota import (
    create_random_block_storage_quota,
    create_random_compute_quota,
)
from app.tests.utils.region import create_random_region
from app.tests.utils.service import (
    create_random_block_storage_service,
    create_random_compute_service,
    create_random_network_service,
)
from app.user_group.models import UserGroup
from fastapi.testclient import TestClient
from neomodel import clear_neo4j_database, db

pytest.register_assert_rewrite(
    "tests.utils.flavor",
    "tests.utils.identity_provider",
    "tests.utils.image",
    "tests.utils.location",
    "tests.utils.network",
    "tests.utils.project",
    "tests.utils.provider",
    "tests.utils.quota",
    "tests.utils.region",
    "tests.utils.service",
    "tests.utils.sla",
    "tests.utils.user_group",
)


@pytest.fixture
def setup_and_teardown_db() -> Generator:
    clear_neo4j_database(db)
    yield
    clear_neo4j_database(db)


@pytest.fixture
def db_provider(setup_and_teardown_db: Generator) -> Provider:
    item_in = create_random_provider()
    item = provider.create(obj_in=item_in)
    yield item


@pytest.fixture
def db_provider_with_project(db_provider: Provider) -> Provider:
    item_in = create_random_project()
    project.create(obj_in=item_in, provider=db_provider)
    yield db_provider


@pytest.fixture
def db_idp(db_provider_with_project: Provider) -> IdentityProvider:
    item_in = create_random_identity_provider(
        projects=[i.uuid for i in db_provider_with_project.projects]
    )
    item = identity_provider.create(obj_in=item_in, provider=db_provider_with_project)
    yield item


@pytest.fixture
def db_group(db_idp: IdentityProvider) -> UserGroup:
    yield db_idp.user_groups.all()[0]


@pytest.fixture
def db_sla(db_group: UserGroup) -> SLA:
    yield db_group.slas.all()[0]


@pytest.fixture
def db_region(db_provider_with_project: Provider) -> Region:
    item_in = create_random_region()
    item = region.create(obj_in=item_in, provider=db_provider_with_project)
    yield item


@pytest.fixture
def db_region2(db_provider_with_project: Provider) -> Region:
    item_in = create_random_region()
    item = region.create(obj_in=item_in, provider=db_provider_with_project)
    yield item


@pytest.fixture
def db_location(db_region: Region) -> Location:
    item_in = create_random_location()
    item = location.create(obj_in=item_in, region=db_region)
    yield item


@pytest.fixture
def db_location2(db_region2: Region) -> Location:
    item_in = create_random_location()
    item = location.create(obj_in=item_in, region=db_region2)
    yield item


@pytest.fixture
def db_block_storage_serv(db_region: Region) -> ComputeService:
    item_in = create_random_block_storage_service()
    item = block_storage_service.create(obj_in=item_in, region=db_region)
    yield item


@pytest.fixture
def db_compute_serv(db_region: Region) -> ComputeService:
    item_in = create_random_compute_service()
    item = compute_service.create(obj_in=item_in, region=db_region)
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
def db_block_storage_quota(
    db_block_storage_serv: BlockStorageService,
) -> BlockStorageQuota:
    db_region = db_block_storage_serv.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.all()[0]
    item_in = create_random_block_storage_quota(project=db_project.uuid)
    item = block_storage_quota.create(
        obj_in=item_in, service=db_block_storage_serv, project=db_project
    )
    yield item


@pytest.fixture
def db_compute_quota(db_compute_serv: ComputeService) -> ComputeQuota:
    db_region = db_compute_serv.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.all()[0]
    item_in = create_random_compute_quota(project=db_project.uuid)
    item = compute_quota.create(
        obj_in=item_in, service=db_compute_serv, project=db_project
    )
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
    return (read_header, write_header)
