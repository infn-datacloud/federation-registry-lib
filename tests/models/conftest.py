"""File to set tests configuration parameters and model fixtures."""
# import os
# from uuid import uuid4
from typing import Any, Generator

import pytest
from neomodel import db

from fedreg.flavor.models import Flavor  # , PrivateFlavor, SharedFlavor
from fedreg.identity_provider.models import IdentityProvider
from fedreg.image.models import Image  # , PrivateImage, SharedImage
from fedreg.location.models import Location
from fedreg.network.models import Network  # , PrivateNetwork, SharedNetwork
from fedreg.project.models import Project
from fedreg.provider.models import Provider
from fedreg.quota.models import (
    BlockStorageQuota,
    ComputeQuota,
    NetworkQuota,
    ObjectStoreQuota,
    Quota,
)
from fedreg.region.models import Region
from fedreg.service.models import (
    BlockStorageService,
    ComputeService,
    IdentityService,
    NetworkService,
    ObjectStoreService,
    Service,
)
from fedreg.sla.models import SLA
from fedreg.user_group.models import UserGroup
from tests.models.utils import (
    flavor_model_dict,
    identity_provider_model_dict,
    image_model_dict,
    location_model_dict,
    network_model_dict,
    project_model_dict,
    provider_model_dict,
    quota_model_dict,
    region_model_dict,
    service_model_dict,
    sla_model_dict,
    user_group_model_dict,
)


@pytest.fixture(scope="session", autouse=True)
def setup_neo4j_session(request):
    """
    Provides initial connection to the database and sets up the rest of the test suite

    :param request: The request object. Please see <https://docs.pytest.org/en/latest/reference.html#_pytest.hookspec.pytest_sessionstart>`_
    :type Request object: For more information please see <https://docs.pytest.org/en/latest/reference.html#request>`_
    """
    # settings.NEO4J_DB_URL = os.environ.get(
    #     "NEO4J_TEST_URL", "bolt://neo4j:password@localhost:7687"
    # )

    # Clear the database if required
    database_is_populated, _ = db.cypher_query(
        "MATCH (a) return count(a)>0 as database_is_populated"
    )
    if database_is_populated[0][0]:
        if not request.config.getoption("resetdb"):
            raise SystemError(
                "Please note: The database seems to be populated.\n"
                + "\tEither delete all nodesand edges manually, or set the "
                + "--resetdb parameter when calling pytest\n\n"
                + "\tpytest --resetdb."
            )

        db.clear_neo4j_database(clear_constraints=True, clear_indexes=True)
        db.install_all_labels()

    db.cypher_query(
        "CREATE OR REPLACE USER test SET PASSWORD 'foobarbaz' CHANGE NOT REQUIRED"
    )
    if db.database_edition == "enterprise":
        db.cypher_query("GRANT ROLE publisher TO test")
        db.cypher_query("GRANT IMPERSONATE (test) ON DBMS TO admin")


@pytest.fixture(autouse=True)
def cleanup() -> Generator[None, Any, None]:
    """Clear DB after every test

    Yields:
        Generator[None, Any, None]: Nothing
    """
    yield
    db.clear_neo4j_database()


@pytest.fixture
def flavor_model() -> Flavor:
    return Flavor(**flavor_model_dict()).save()


# @pytest.fixture
# def private_flavor_model() -> PrivateFlavor:
#     return PrivateFlavor(**flavor_model_dict()).save()


# @pytest.fixture
# def shared_flavor_model() -> SharedFlavor:
#     return SharedFlavor(**flavor_model_dict()).save()


@pytest.fixture
def identity_provider_model() -> IdentityProvider:
    return IdentityProvider(**identity_provider_model_dict()).save()


@pytest.fixture
def image_model() -> Image:
    return Image(**image_model_dict()).save()


# @pytest.fixture
# def private_image_model() -> PrivateImage:
#     return PrivateImage(**image_model_dict()).save()


# @pytest.fixture
# def shared_image_model() -> SharedImage:
#     return SharedImage(**image_model_dict()).save()


@pytest.fixture
def location_model() -> Location:
    return Location(**location_model_dict()).save()


@pytest.fixture
def network_model() -> Network:
    return Network(**network_model_dict()).save()


# @pytest.fixture
# def private_network_model() -> PrivateNetwork:
#     return PrivateNetwork(**network_model_dict()).save()


# @pytest.fixture
# def shared_network_model() -> SharedNetwork:
#     return SharedNetwork(**network_model_dict()).save()


@pytest.fixture
def project_model() -> Project:
    return Project(**project_model_dict()).save()


@pytest.fixture
def provider_model() -> Provider:
    return Provider(**provider_model_dict()).save()


@pytest.fixture
def quota_model() -> Quota:
    return Quota(**quota_model_dict()).save()


@pytest.fixture
def block_storage_quota_model() -> BlockStorageQuota:
    return BlockStorageQuota(**quota_model_dict()).save()


@pytest.fixture
def compute_quota_model() -> ComputeQuota:
    return ComputeQuota(**quota_model_dict()).save()


@pytest.fixture
def network_quota_model() -> NetworkQuota:
    return NetworkQuota(**quota_model_dict()).save()


@pytest.fixture
def object_store_quota_model() -> ObjectStoreQuota:
    return ObjectStoreQuota(**quota_model_dict()).save()


@pytest.fixture
def region_model() -> Region:
    return Region(**region_model_dict()).save()


@pytest.fixture
def service_model() -> Service:
    return Service(**service_model_dict()).save()


@pytest.fixture
def block_storage_service_model() -> BlockStorageService:
    return BlockStorageService(**service_model_dict()).save()


@pytest.fixture
def compute_service_model() -> ComputeService:
    return ComputeService(**service_model_dict()).save()


@pytest.fixture
def identity_service_model() -> IdentityService:
    return IdentityService(**service_model_dict()).save()


@pytest.fixture
def network_service_model() -> NetworkService:
    return NetworkService(**service_model_dict()).save()


@pytest.fixture
def object_store_service_model() -> ObjectStoreService:
    return ObjectStoreService(**service_model_dict()).save()


@pytest.fixture
def sla_model() -> SLA:
    return SLA(**sla_model_dict()).save()


@pytest.fixture
def user_group_model() -> UserGroup:
    return UserGroup(**user_group_model_dict()).save()
