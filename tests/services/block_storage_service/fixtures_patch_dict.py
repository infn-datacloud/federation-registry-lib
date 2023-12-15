"""BlockStorageService specific fixtures."""
from typing import Any, Dict

from pytest_cases import fixture, parametrize

from app.service.enum import ServiceType
from tests.utils.block_storage_service import random_block_storage_service_name
from tests.utils.compute_service import random_compute_service_name
from tests.utils.identity_service import random_identity_service_name
from tests.utils.network_service import random_network_service_name
from tests.utils.utils import random_lower_string, random_url

patch_key_values = [
    ("description", random_lower_string()),
    ("endpoint", random_url()),
    ("name", random_block_storage_service_name()),
]
invalid_patch_key_values = [  # None is not accepted because there is a default
    ("description", None),
    ("type", None),
    ("type", ServiceType.COMPUTE),
    ("type", ServiceType.IDENTITY),
    ("type", ServiceType.NETWORK),
    ("name", random_lower_string()),
    ("name", random_compute_service_name()),
    ("name", random_identity_service_name()),
    ("name", random_network_service_name()),
]


@fixture
@parametrize("k, v", patch_key_values)
def block_storage_service_patch_valid_data(k: str, v: Any) -> Dict[str, Any]:
    """Valid set of single key-value pair for a BlockStorageService patch schema."""
    return {k: v}


@fixture
@parametrize("k, v", invalid_patch_key_values)
def block_storage_service_patch_invalid_data(k: str, v: Any) -> Dict[str, Any]:
    """Invalid set of attributes for a BlockStorageService patch schema."""
    return {k: v}
