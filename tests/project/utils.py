"""Project utilities."""

from typing import Any, Dict
from uuid import uuid4

from tests.common.utils import random_lower_string


def random_project_required_attr() -> Dict[str, Any]:
    """Return a dict with the Project required attributes initialized."""
    return {"name": random_lower_string(), "uuid": uuid4()}


def random_project_all_attr() -> Dict[str, Any]:
    """Dict with all Project attributes."""
    return {**random_project_required_attr(), "description": random_lower_string()}
