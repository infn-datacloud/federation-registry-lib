"""IdentityProvider utilities."""
from typing import Any, Dict

from tests.common.utils import random_lower_string, random_url
from tests.user_group.utils import (
    random_user_group_required_attr,
    random_user_group_required_rel,
)


def random_identity_provider_required_attr() -> Dict[str, Any]:
    """Return a dict with the IdentityProvider required attributes initialized."""
    return {"endpoint": random_url(), "group_claim": random_lower_string()}


def random_identity_provider_all_attr() -> Dict[str, Any]:
    """Dict with all IdentityProvider attributes."""
    return {
        **random_identity_provider_required_attr(),
        "description": random_lower_string(),
    }


def random_identity_provider_required_rel() -> Dict[str, Any]:
    """Return a dict with the IdentityProvider required relationships initialized."""
    return {
        "relationship": {
            "idp_name": random_lower_string(),
            "protocol": random_lower_string(),
        },
        "user_groups": [
            {**random_user_group_required_attr(), **random_user_group_required_rel()}
        ],
    }
