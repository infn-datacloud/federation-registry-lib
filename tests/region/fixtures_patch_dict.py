"""Region specific fixtures."""
import copy
from typing import Any, Dict

from pytest_cases import fixture, parametrize

from app.region.models import Region
from app.region.schemas import RegionUpdate
from tests.common.utils import random_bool, random_lower_string
from tests.services.block_storage_service.utils import (
    random_block_storage_service_required_attr,
)
from tests.services.compute_service.utils import random_compute_service_required_attr
from tests.services.identity_service.utils import random_identity_service_required_attr
from tests.services.network_service.utils import random_network_service_required_attr

patch_key_values = [
    ("description", random_lower_string()),
    ("name", random_lower_string()),
]
invalid_patch_key_values = [  # None is not accepted because there is a default
    ("description", None)
]


@fixture
@parametrize("k, v", patch_key_values)
def region_patch_valid_data(k: str, v: Any) -> Dict[str, Any]:
    """Valid set of single key-value pair for a Region patch schema."""
    return {k: v}


@fixture
@parametrize("k, v", invalid_patch_key_values)
def region_patch_invalid_data(k: str, v: Any) -> Dict[str, Any]:
    """Invalid set of attributes for a Region patch schema."""
    return {k: v}


def region_patch_not_equal_data(
    *, db_item: Region, new_data: Dict[str, Any]
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
            schema_type = RegionUpdate.__fields__.get(k).type_
            if schema_type == bool:
                valid_data[k] = random_bool()
            else:
                print(schema_type)
                assert 0
    return valid_data


def region_force_update_enriched_relationships_data(
    data: Dict[str, Any],
) -> Dict[str, Any]:
    """Generate a copy of the input data and add new items to empty lists."""
    new_data = copy.deepcopy(data)
    if len(new_data.get("block_storage_services", [])) > 0:
        new_data["block_storage_services"].append(
            random_block_storage_service_required_attr()
        )
    if len(new_data.get("compute_services", [])) > 0:
        new_data["compute_services"].append(random_compute_service_required_attr())
    if len(new_data.get("identity_services", [])) > 0:
        new_data["identity_services"].append(random_identity_service_required_attr())
    if len(new_data.get("network_services", [])) > 0:
        new_data["network_services"].append(random_network_service_required_attr())
    return new_data
