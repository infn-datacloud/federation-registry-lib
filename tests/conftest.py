"""File to set tests configuration parameters and common fixtures."""
import os
from typing import Any, Generator
from unittest.mock import MagicMock, PropertyMock, patch
from uuid import uuid4

import pytest
from neo4j.graph import Node

from fed_reg.flavor.models import Flavor
from fed_reg.project.models import Project
from fed_reg.service.models import ComputeService
from tests.create_dict import flavor_dict, project_dict, service_dict

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
    d = flavor_dict()
    element_id = f"{db_core.database_version}:{uuid4().hex}:{FLAVOR_ID}"
    db_core.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=FLAVOR_ID, properties=d)]],
        None,
    )
    return Flavor(**d).save()


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
def compute_service_model(db_core: MagicMock) -> ComputeService:
    d = service_dict()
    element_id = f"{db_core.database_version}:{uuid4().hex}:{COMPUTE_SERVICE_ID}"
    db_core.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=COMPUTE_SERVICE_ID, properties=d)]],
        None,
    )
    return ComputeService(**d).save()
