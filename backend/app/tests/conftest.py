from typing import Generator

import pytest
from app.identity_provider.crud import identity_provider
from app.identity_provider.models import IdentityProvider
from app.main import app
from app.project.crud import project
from app.provider.crud import provider
from app.provider.models import Provider
from app.region.crud import region
from app.region.models import Region
from app.service.crud import block_storage_service, compute_service, network_service
from app.service.models import ComputeService, NetworkService
from app.tests.utils.identity_provider import create_random_identity_provider
from app.tests.utils.project import create_random_project
from app.tests.utils.provider import create_random_provider
from app.tests.utils.region import create_random_region
from app.tests.utils.service import (
    create_random_block_storage_service,
    create_random_compute_service,
    create_random_network_service,
)
from app.tests.utils.user_group import create_random_user_group
from app.user_group.crud import user_group
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
def db_idp(db_provider: Provider) -> IdentityProvider:
    item_in = create_random_project()
    item = project.create(obj_in=item_in, provider=db_provider)
    item_in = create_random_identity_provider()
    item = identity_provider.create(obj_in=item_in, provider=db_provider)
    yield item


@pytest.fixture
def db_group(db_idp: IdentityProvider) -> UserGroup:
    item_in = create_random_user_group()
    item = user_group.create(obj_in=item_in, identity_provider=db_idp)
    yield item


@pytest.fixture
def db_region(db_provider: Provider) -> Region:
    item_in = create_random_project()
    item = project.create(obj_in=item_in, provider=db_provider)
    item_in = create_random_region()
    item = region.create(obj_in=item_in, provider=db_provider)
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
def db_network_serv(db_region: Region) -> NetworkService:
    item_in = create_random_network_service()
    item = network_service.create(obj_in=item_in, region=db_region)
    yield item


@pytest.fixture
def client(setup_and_teardown_db: Generator) -> Generator:
    with TestClient(app) as c:
        yield c
