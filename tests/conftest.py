"""File to set tests configuration parameters and common fixtures."""
import os
from uuid import uuid4

import pytest

from fed_reg.project.models import Project
from fed_reg.service.models import ComputeService
from tests.common.utils import random_lower_string


@pytest.fixture(autouse=True)
def clear_os_environment() -> None:
    """Clear the OS environment."""
    os.environ.clear()


@pytest.fixture
def project_model() -> Project:
    return Project(name=random_lower_string(), uuid=uuid4().hex)


@pytest.fixture
def compute_service_model() -> ComputeService:
    return ComputeService(
        name=random_lower_string(),
        endpoint=random_lower_string(),
        type=random_lower_string(),
    )
