"""Image specific fixtures."""
from typing import Any, Dict
from uuid import uuid4

from pytest_cases import fixture, fixture_union, parametrize

from tests.utils.image import random_os_type
from tests.utils.utils import random_bool, random_lower_string

patch_key_values = {
    ("description", random_lower_string()),
    ("uuid", uuid4()),
    ("name", random_lower_string()),
    ("os_type", random_os_type()),
    ("os_distro", random_lower_string()),
    ("os_version", random_lower_string()),
    ("architecture", random_lower_string()),
    ("kernel_id", random_lower_string()),
    ("cuda_support", random_bool()),
    ("gpu_driver", random_bool()),
}
invalid_patch_key_values = {  # None is not accepted because there is a default
    ("description", None),
    ("is_public", None),
    ("cuda_support", None),
    ("gpu_driver", None),
    ("tags", None),
}


@fixture
@parametrize("k, v", patch_key_values)
def image_patch_valid_data_single_attr(k: str, v: Any) -> Dict[str, Any]:
    """Valid set of single key-value pair for a Image patch schema."""
    return {k: v}


@fixture
def image_patch_valid_data_for_tags() -> Dict[str, Any]:
    """Valid set of attributes for a Image patch schema. Tags details."""
    return {"tags": [random_lower_string()]}


image_patch_valid_data = fixture_union(
    "image_patch_valid_data",
    (image_patch_valid_data_single_attr, image_patch_valid_data_for_tags),
    idstyle="explicit",
)


@fixture
@parametrize("k, v", invalid_patch_key_values)
def image_patch_invalid_data(k: str, v: Any) -> Dict[str, Any]:
    """Invalid set of attributes for a Image patch schema."""
    return {k: v}
