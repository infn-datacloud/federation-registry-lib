"""File to set tests configuration parameters and common fixtures."""
import os

import pytest


@pytest.fixture(autouse=True)
def clear_os_environment() -> None:
    """Clear the OS environment."""
    os.environ.clear()
