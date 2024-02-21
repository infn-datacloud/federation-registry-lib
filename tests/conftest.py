"""File to set tests configuration parameters and common fixtures."""
import os
from typing import Any, Generator
from unittest.mock import MagicMock, PropertyMock, patch
from uuid import uuid4

import pytest
from neo4j.graph import Node

from fed_reg.flavor.models import Flavor
from fed_reg.identity_provider.models import IdentityProvider
from fed_reg.image.models import Image
from fed_reg.location.models import Location
from fed_reg.network.models import Network
from fed_reg.project.models import Project
from fed_reg.provider.models import Provider
from fed_reg.quota.models import BlockStorageQuota, ComputeQuota, NetworkQuota
from fed_reg.region.models import Region
from fed_reg.service.models import (
    BlockStorageService,
    ComputeService,
    IdentityService,
    NetworkService,
)
from fed_reg.sla.models import SLA
from fed_reg.user_group.models import UserGroup
from tests.create_dict import (
    flavor_model_dict,
    identity_provider_model_dict,
    image_dict,
    location_dict,
    network_dict,
    project_dict,
    provider_dict,
    quota_dict,
    region_dict,
    service_dict,
    sla_dict,
    user_group_dict,
)

FLAVOR_ID = 10
IDENTITY_PROVIDER_ID = 20
IMAGE_ID = 30
LOCATION_ID = 40
NETWORK_ID = 50
PROJECT_ID = 60
PROVIDER_ID = 70
BLOCK_STORAGE_QUOTA_ID = 80
COMPUTE_QUOTA_ID = 90
NETWORK_QUOTA_ID = 100
REGION_ID = 110
BLOCK_STORAGE_SERVICE_ID = 120
COMPUTE_SERVICE_ID = 130
IDENTITY_SERVICE_ID = 140
NETWORK_SERVICE_ID = 150
SLA_ID = 160
USER_GROUP_ID = 170

DB_VERSION = "5"


@pytest.fixture(autouse=True)
def clear_os_environment() -> None:
    """Clear the OS environment."""
    os.environ.clear()


@pytest.fixture(scope="session")
def db_core() -> Generator[MagicMock, Any, None]:
    with patch("neomodel.core.db") as mock_db:
        type(mock_db).database_version = PropertyMock(return_value=DB_VERSION)
        yield mock_db


@pytest.fixture(scope="session")
def db_match() -> Generator[MagicMock, Any, None]:
    with patch("neomodel.match.db") as mock_db:
        type(mock_db).database_version = PropertyMock(return_value=DB_VERSION)
        yield mock_db


@pytest.fixture(scope="session")
def db_rel_mgr() -> Generator[MagicMock, Any, None]:
    with patch("neomodel.relationship_manager.db") as mock_db:
        type(mock_db).database_version = PropertyMock(return_value=DB_VERSION)

        d = {}
        cls_registry = MagicMock()
        cls_registry.__getitem__.side_effect = d.__getitem__
        cls_registry.__setitem__.side_effect = d.__setitem__
        mock_db._NODE_CLASS_REGISTRY = cls_registry

        yield mock_db


@pytest.fixture
def flavor_model(db_core: MagicMock) -> Flavor:
    d = flavor_model_dict()
    element_id = f"{db_core.database_version}:{uuid4().hex}:{FLAVOR_ID}"
    db_core.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=FLAVOR_ID, properties=d)]],
        None,
    )
    return Flavor(**d).save()


@pytest.fixture
def identity_provider_model(db_core: MagicMock) -> IdentityProvider:
    d = identity_provider_model_dict()
    element_id = f"{db_core.database_version}:{uuid4().hex}:{IDENTITY_PROVIDER_ID}"
    db_core.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=IDENTITY_PROVIDER_ID, properties=d)]],
        None,
    )
    return IdentityProvider(**d).save()


@pytest.fixture
def image_model(db_core: MagicMock) -> Image:
    d = image_dict()
    element_id = f"{db_core.database_version}:{uuid4().hex}:{IMAGE_ID}"
    db_core.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=IMAGE_ID, properties=d)]],
        None,
    )
    return Image(**d).save()


@pytest.fixture
def location_model(db_core: MagicMock) -> Location:
    d = location_dict()
    element_id = f"{db_core.database_version}:{uuid4().hex}:{LOCATION_ID}"
    db_core.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=LOCATION_ID, properties=d)]],
        None,
    )
    return Location(**d).save()


@pytest.fixture
def network_model(db_core: MagicMock) -> Network:
    d = network_dict()
    element_id = f"{db_core.database_version}:{uuid4().hex}:{NETWORK_ID}"
    db_core.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=NETWORK_ID, properties=d)]],
        None,
    )
    return Network(**d).save()


@pytest.fixture
def project_model(db_core: MagicMock) -> Project:
    d = project_dict()
    element_id = f"{db_core.database_version}:{uuid4().hex}:{PROJECT_ID}"
    db_core.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=PROJECT_ID, properties=d)]],
        None,
    )
    return Project(**d).save()


@pytest.fixture
def provider_model(db_core: MagicMock) -> Provider:
    d = provider_dict()
    element_id = f"{db_core.database_version}:{uuid4().hex}:{PROVIDER_ID}"
    db_core.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=PROVIDER_ID, properties=d)]],
        None,
    )
    return Provider(**d).save()


@pytest.fixture
def block_storage_quota_model(db_core: MagicMock) -> BlockStorageQuota:
    d = quota_dict()
    element_id = f"{db_core.database_version}:{uuid4().hex}:{BLOCK_STORAGE_QUOTA_ID}"
    db_core.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=BLOCK_STORAGE_QUOTA_ID, properties=d)]],
        None,
    )
    return BlockStorageQuota(**d).save()


@pytest.fixture
def compute_quota_model(db_core: MagicMock) -> ComputeQuota:
    d = quota_dict()
    element_id = f"{db_core.database_version}:{uuid4().hex}:{COMPUTE_QUOTA_ID}"
    db_core.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=COMPUTE_QUOTA_ID, properties=d)]],
        None,
    )
    return ComputeQuota(**d).save()


@pytest.fixture
def network_quota_model(db_core: MagicMock) -> NetworkQuota:
    d = quota_dict()
    element_id = f"{db_core.database_version}:{uuid4().hex}:{NETWORK_QUOTA_ID}"
    db_core.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=NETWORK_QUOTA_ID, properties=d)]],
        None,
    )
    return NetworkQuota(**d).save()


@pytest.fixture
def region_model(db_core: MagicMock) -> Region:
    d = region_dict()
    element_id = f"{db_core.database_version}:{uuid4().hex}:{REGION_ID}"
    db_core.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=REGION_ID, properties=d)]],
        None,
    )
    return Region(**d).save()


@pytest.fixture
def block_storage_service_model(db_core: MagicMock) -> BlockStorageService:
    d = service_dict()
    element_id = f"{db_core.database_version}:{uuid4().hex}:{BLOCK_STORAGE_SERVICE_ID}"
    db_core.cypher_query.return_value = (
        [
            [
                Node(
                    ...,
                    element_id=element_id,
                    id_=BLOCK_STORAGE_SERVICE_ID,
                    properties=d,
                )
            ]
        ],
        None,
    )
    return BlockStorageService(**d).save()


@pytest.fixture
def compute_service_model(db_core: MagicMock) -> ComputeService:
    d = service_dict()
    element_id = f"{db_core.database_version}:{uuid4().hex}:{COMPUTE_SERVICE_ID}"
    db_core.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=COMPUTE_SERVICE_ID, properties=d)]],
        None,
    )
    return ComputeService(**d).save()


@pytest.fixture
def identity_service_model(db_core: MagicMock) -> IdentityService:
    d = service_dict()
    element_id = f"{db_core.database_version}:{uuid4().hex}:{IDENTITY_SERVICE_ID}"
    db_core.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=IDENTITY_SERVICE_ID, properties=d)]],
        None,
    )
    return IdentityService(**d).save()


@pytest.fixture
def network_service_model(db_core: MagicMock) -> NetworkService:
    d = service_dict()
    element_id = f"{db_core.database_version}:{uuid4().hex}:{NETWORK_SERVICE_ID}"
    db_core.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=NETWORK_SERVICE_ID, properties=d)]],
        None,
    )
    return NetworkService(**d).save()


@pytest.fixture
def sla_model(db_core: MagicMock) -> SLA:
    d = sla_dict()
    element_id = f"{db_core.database_version}:{uuid4().hex}:{SLA_ID}"
    db_core.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=SLA_ID, properties=d)]],
        None,
    )
    return SLA(**d).save()


@pytest.fixture
def user_group_model(db_core: MagicMock) -> UserGroup:
    d = user_group_dict()
    element_id = f"{db_core.database_version}:{uuid4().hex}:{USER_GROUP_ID}"
    db_core.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=USER_GROUP_ID, properties=d)]],
        None,
    )
    return UserGroup(**d).save()
