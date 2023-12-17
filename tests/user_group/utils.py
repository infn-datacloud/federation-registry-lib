"""UserGroup utilities."""
from typing import Any, Dict

from tests.common.utils import random_lower_string
from tests.sla.utils import random_sla_required_attr, random_sla_required_rel


def random_user_group_required_attr() -> Dict[str, Any]:
    """Dict with UserGroup mandatory attributes."""
    return {"name": random_lower_string()}


def random_user_group_all_attr() -> Dict[str, Any]:
    """Dict with all UserGroup attributes."""
    return {**random_user_group_required_attr(), "description": random_lower_string()}


def random_user_group_required_rel() -> Dict[str, Any]:
    """Dict with all UserGroup required relationships initialized."""
    return {"sla": {**random_sla_required_attr(), **random_sla_required_rel()}}
