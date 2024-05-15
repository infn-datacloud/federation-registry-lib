"""File to set tests configuration parameters and common fixtures."""
import os
from typing import Any, Generator
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from flaat.user_infos import UserInfos
from neomodel import db

from fed_reg.flavor.models import Flavor
from fed_reg.identity_provider.models import IdentityProvider
from fed_reg.image.models import Image
from fed_reg.location.models import Location
from fed_reg.location.schemas import LocationCreate
from fed_reg.main import app
from fed_reg.network.models import Network
from fed_reg.project.models import Project
from fed_reg.project.schemas import ProjectCreate
from fed_reg.provider.models import Provider
from fed_reg.provider.schemas_extended import (
    BlockStorageQuotaCreateExtended,
    BlockStorageServiceCreateExtended,
    ComputeQuotaCreateExtended,
    ComputeServiceCreateExtended,
    FlavorCreateExtended,
    IdentityProviderCreateExtended,
    ImageCreateExtended,
    NetworkCreateExtended,
    NetworkQuotaCreateExtended,
    NetworkServiceCreateExtended,
    ProviderCreateExtended,
    RegionCreateExtended,
    SLACreateExtended,
    UserGroupCreateExtended,
)
from fed_reg.quota.models import BlockStorageQuota, ComputeQuota, NetworkQuota
from fed_reg.region.models import Region
from fed_reg.service.models import (
    BlockStorageService,
    ComputeService,
    IdentityService,
    NetworkService,
)
from fed_reg.service.schemas import IdentityServiceCreate
from fed_reg.sla.models import SLA
from fed_reg.user_group.models import UserGroup
from tests.create_dict import (
    auth_method_dict,
    block_storage_quota_model_dict,
    block_storage_service_model_dict,
    block_storage_service_schema_dict,
    compute_quota_model_dict,
    compute_service_model_dict,
    compute_service_schema_dict,
    flavor_model_dict,
    flavor_schema_dict,
    identity_provider_model_dict,
    identity_provider_schema_dict,
    identity_service_model_dict,
    identity_service_schema_dict,
    image_model_dict,
    image_schema_dict,
    location_model_dict,
    location_schema_dict,
    network_model_dict,
    network_quota_model_dict,
    network_schema_dict,
    network_service_model_dict,
    network_service_schema_dict,
    project_model_dict,
    project_schema_dict,
    provider_model_dict,
    provider_schema_dict,
    region_model_dict,
    region_schema_dict,
    sla_model_dict,
    sla_schema_dict,
    user_group_model_dict,
    user_group_schema_dict,
)
from tests.utils import MOCK_READ_EMAIL, MOCK_WRITE_EMAIL


def pytest_addoption(parser):
    """
    Adds the command line option --resetdb.

    :param parser: The parser object. Please see <https://docs.pytest.org/en/latest/reference.html#_pytest.hookspec.pytest_addoption>`_
    :type Parser object: For more information please see <https://docs.pytest.org/en/latest/reference.html#_pytest.config.Parser>`_
    """
    parser.addoption(
        "--resetdb",
        action="store_true",
        help="Ensures that the database is clear prior to running tests for neomodel",
        default=False,
    )


@pytest.fixture(scope="session", autouse=True)
def setup_neo4j_session(request):
    """
    Provides initial connection to the database and sets up the rest of the test suite

    :param request: The request object. Please see <https://docs.pytest.org/en/latest/reference.html#_pytest.hookspec.pytest_sessionstart>`_
    :type Request object: For more information please see <https://docs.pytest.org/en/latest/reference.html#request>`_
    """
    # config.DATABASE_URL = os.environ.get(
    #     "NEO4J_BOLT_URL", "bolt://localhost:7687"
    # )

    # Clear the database if required
    database_is_populated, _ = db.cypher_query(
        "MATCH (a) return count(a)>0 as database_is_populated"
    )
    if database_is_populated[0][0] and not request.config.getoption("resetdb"):
        raise SystemError(
            "Please note: The database seems to be populated.\n"
            + "\tEither delete all nodesand edges manually, or set the "
            + "--resetdb parameter when calling pytest\n\n"
            + "\tpytest --resetdb."
        )

    # db.clear_neo4j_database(clear_constraints=True, clear_indexes=True)

    # db.install_all_labels()

    db.cypher_query(
        "CREATE OR REPLACE USER test SET PASSWORD 'foobarbaz' CHANGE NOT REQUIRED"
    )
    if db.database_edition == "enterprise":
        db.cypher_query("GRANT ROLE publisher TO test")
        db.cypher_query("GRANT IMPERSONATE (test) ON DBMS TO admin")


@pytest.fixture(scope="session", autouse=True)
def cleanup() -> Generator[None, Any, None]:
    """Close connection with the DB at the end of the test.

    Yields:
        Generator[None, Any, None]: Nothing
    """
    yield
    db.clear_neo4j_database()
    db.close_connection()


@pytest.fixture(autouse=True)
def clear_os_environment() -> None:
    """Clear the OS environment."""
    os.environ.clear()


@pytest.fixture
def flavor_model() -> Flavor:
    d = flavor_model_dict()
    return Flavor(**d).save()


@pytest.fixture
def identity_provider_model() -> IdentityProvider:
    d = identity_provider_model_dict()
    return IdentityProvider(**d).save()


@pytest.fixture
def image_model() -> Image:
    d = image_model_dict()
    return Image(**d).save()


@pytest.fixture
def location_model() -> Location:
    d = location_model_dict()
    return Location(**d).save()


@pytest.fixture
def network_model() -> Network:
    d = network_model_dict()
    return Network(**d).save()


@pytest.fixture
def project_model() -> Project:
    d = project_model_dict()
    return Project(**d).save()


@pytest.fixture
def provider_model() -> Provider:
    d = provider_model_dict()
    return Provider(**d).save()


@pytest.fixture
def block_storage_quota_model() -> BlockStorageQuota:
    d = block_storage_quota_model_dict()
    return BlockStorageQuota(**d).save()


@pytest.fixture
def compute_quota_model() -> ComputeQuota:
    d = compute_quota_model_dict()
    return ComputeQuota(**d).save()


@pytest.fixture
def network_quota_model() -> NetworkQuota:
    d = network_quota_model_dict()
    return NetworkQuota(**d).save()


@pytest.fixture
def region_model() -> Region:
    d = region_model_dict()
    return Region(**d).save()


@pytest.fixture
def block_storage_service_model() -> BlockStorageService:
    d = block_storage_service_model_dict()
    return BlockStorageService(**d).save()


@pytest.fixture
def compute_service_model() -> ComputeService:
    d = compute_service_model_dict()
    return ComputeService(**d).save()


@pytest.fixture
def identity_service_model() -> IdentityService:
    d = identity_service_model_dict()
    return IdentityService(**d).save()


@pytest.fixture
def network_service_model() -> NetworkService:
    d = network_service_model_dict()
    return NetworkService(**d).save()


@pytest.fixture
def sla_model() -> SLA:
    d = sla_model_dict()
    return SLA(**d).save()


@pytest.fixture
def user_group_model() -> UserGroup:
    d = user_group_model_dict()
    return UserGroup(**d).save()


@pytest.fixture
def location_create_schema() -> LocationCreate:
    return LocationCreate(**location_schema_dict())


@pytest.fixture
def project_create_schema() -> ProjectCreate:
    return ProjectCreate(**project_schema_dict())


@pytest.fixture
def identity_service_create_schema() -> IdentityServiceCreate:
    return IdentityServiceCreate(**identity_service_schema_dict())


@pytest.fixture
def flavor_create_ext_schema() -> FlavorCreateExtended:
    return FlavorCreateExtended(**flavor_schema_dict())


@pytest.fixture
def identity_provider_create_ext_schema(
    user_group_create_ext_schema: UserGroupCreateExtended,
) -> IdentityProviderCreateExtended:
    return IdentityProviderCreateExtended(
        **identity_provider_schema_dict(),
        relationship=auth_method_dict(),
        user_groups=[user_group_create_ext_schema],
    )


@pytest.fixture
def image_create_ext_schema() -> ImageCreateExtended:
    return ImageCreateExtended(**image_schema_dict())


@pytest.fixture
def network_create_ext_schema() -> NetworkCreateExtended:
    return NetworkCreateExtended(**network_schema_dict())


@pytest.fixture
def provider_create_ext_schema() -> ProviderCreateExtended:
    return ProviderCreateExtended(**provider_schema_dict())


@pytest.fixture
def block_storage_quota_create_ext_schema() -> BlockStorageQuotaCreateExtended:
    return BlockStorageQuotaCreateExtended(project=uuid4())


@pytest.fixture
def compute_quota_create_ext_schema() -> ComputeQuotaCreateExtended:
    return ComputeQuotaCreateExtended(project=uuid4())


@pytest.fixture
def network_quota_create_ext_schema() -> NetworkQuotaCreateExtended:
    return NetworkQuotaCreateExtended(project=uuid4())


@pytest.fixture
def region_create_ext_schema() -> RegionCreateExtended:
    return RegionCreateExtended(**region_schema_dict())


@pytest.fixture
def block_storage_service_create_ext_schema() -> BlockStorageServiceCreateExtended:
    return BlockStorageServiceCreateExtended(**block_storage_service_schema_dict())


@pytest.fixture
def compute_service_create_ext_schema() -> ComputeServiceCreateExtended:
    return ComputeServiceCreateExtended(**compute_service_schema_dict())


@pytest.fixture
def network_service_create_ext_schema() -> NetworkServiceCreateExtended:
    return NetworkServiceCreateExtended(**network_service_schema_dict())


@pytest.fixture
def sla_create_ext_schema() -> SLACreateExtended:
    return SLACreateExtended(**sla_schema_dict(), project=uuid4())


@pytest.fixture
def user_group_create_ext_schema(
    sla_create_ext_schema: SLACreateExtended,
) -> UserGroupCreateExtended:
    return UserGroupCreateExtended(
        **user_group_schema_dict(), sla=sla_create_ext_schema
    )


@pytest.fixture
def client_no_authn():
    with TestClient(app) as client:
        yield client


@pytest.fixture
def client_with_token(client_no_authn: TestClient):
    client_no_authn.headers = {"Authorization": "Bearer fake"}
    return client_no_authn

@pytest.fixture
def user_infos_with_write_email() -> UserInfos:
    """Fake user with email. It has write access rights."""
    return UserInfos(
        access_token_info=None,
        user_info={"email": MOCK_WRITE_EMAIL},
        introspection_info=None,
    )


@pytest.fixture
def user_infos_with_read_email() -> UserInfos:
    """Fake user with email. It has only read access rights."""
    return UserInfos(
        access_token_info=None,
        user_info={"email": MOCK_READ_EMAIL},
        introspection_info=None,
    )


@pytest.fixture
def user_infos_without_email() -> UserInfos:
    """Fake user without email."""
    return UserInfos(access_token_info=None, user_info={}, introspection_info=None)

