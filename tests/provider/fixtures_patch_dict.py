"""Provider specific fixtures."""
import copy
from typing import Any, Dict

from pytest_cases import fixture, fixture_union, parametrize

from app.provider.enum import ProviderStatus, ProviderType
from app.provider.models import Provider
from app.provider.schemas import ProviderUpdate
from tests.common.utils import (
    random_bool,
    random_email,
    random_lower_string,
)
from tests.identity_provider.utils import (
    random_identity_provider_required_attr,
    random_identity_provider_required_rel,
)
from tests.project.utils import random_project_required_attr
from tests.provider.utils import random_status, random_type
from tests.region.utils import random_region_required_attr

patch_key_values = [
    ("description", random_lower_string()),
    ("name", random_lower_string()),
    ("type", random_type()),
    ("status", random_status()),
    ("is_public", random_bool()),
]
invalid_patch_key_values = [  # None is not accepted because there is a default
    ("description", None),
    ("type", random_lower_string()),
    ("status", None),
    ("status", random_lower_string()),
    ("is_public", None),
]


@fixture
@parametrize("k, v", patch_key_values)
def provider_patch_valid_data_single_attr(k: str, v: Any) -> Dict[str, Any]:
    """Valid set of single key-value pair for a Provider patch schema."""
    return {k: v}


@fixture
def provider_patch_valid_data_for_support_emails() -> Dict[str, Any]:
    """Valid set of attributes for a Image patch schema. Tags details."""
    return {"support_emails": [random_email()]}


@fixture
@parametrize("k, v", invalid_patch_key_values)
def provider_patch_invalid_data_single_attr(k: str, v: Any) -> Dict[str, Any]:
    """Invalid set of attributes for a Provider patch schema."""
    return {k: v}


@fixture
@parametrize(support_emails={None, random_lower_string()})
def provider_patch_invalid_data_for_support_emails(support_emails) -> Dict[str, Any]:
    """Valid set of attributes for a Image patch schema. Tags details."""
    support_emails = [support_emails] if support_emails else support_emails
    return {"support_emails": support_emails}


provider_patch_valid_data = fixture_union(
    "provider_patch_valid_data",
    (
        provider_patch_valid_data_single_attr,
        provider_patch_valid_data_for_support_emails,
    ),
    idstyle="explicit",
)


provider_patch_invalid_data = fixture_union(
    "provider_patch_invalid_data",
    (
        provider_patch_invalid_data_single_attr,
        provider_patch_invalid_data_for_support_emails,
    ),
    idstyle="explicit",
)


def provider_patch_not_equal_data(
    *, db_item: Provider, new_data: Dict[str, Any]
) -> Dict[str, Any]:
    """Return a dict with new different data.

    The dict has the same keys as the input dict. If the values in the received dict
    differs from the ones in the DB instance, they are kept, otherwise they are
    substituted.

    Args:
    ----
        db_item (Provider): DB instance.
        new_data (dict): Dict with the initial data.
    """
    valid_data = {}
    for k, v in new_data.items():
        valid_data[k] = v
        while db_item.__getattribute__(k) == valid_data[k]:
            schema_type = ProviderUpdate.__fields__.get(k).type_
            if schema_type == bool:
                valid_data[k] = random_bool()
            elif schema_type == ProviderStatus:
                valid_data[k] = random_status()
            elif schema_type == ProviderType:
                valid_data[k] = random_type()
            else:
                print(schema_type)
                assert 0
    return valid_data


def provider_force_update_enriched_relationships_data(
    data: Dict[str, Any],
) -> Dict[str, Any]:
    """Generate a copy of the input data and add new items to empty lists."""
    new_data = copy.deepcopy(data)
    if len(new_data.get("regions", [])) > 0:
        new_data["regions"].append(random_region_required_attr())
    if len(new_data.get("projects", [])) > 0:
        new_data["projects"].append(random_project_required_attr())
    if len(new_data.get("identity_providers", [])) > 0:
        new_data["identity_providers"].append(
            {
                **random_identity_provider_required_attr(),
                **random_identity_provider_required_rel(),
            }
        )
        new_data["identity_providers"][-1]["user_groups"][0]["sla"][
            "project"
        ] = new_data["projects"][-1]["uuid"]
    return new_data
