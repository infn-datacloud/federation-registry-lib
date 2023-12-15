"""Flavor specific fixtures."""
from typing import Any, Dict
from uuid import uuid4

from pytest_cases import fixture, fixture_union, parametrize

from tests.utils.utils import (
    random_bool,
    random_lower_string,
    random_non_negative_int,
    random_positive_int,
)

gpu_details = [
    ("gpu_model", random_lower_string()),  # gpus is 0
    ("gpu_vendor", random_lower_string()),  # gpus is 0
]
patch_key_values = [
    ("description", random_lower_string()),
    ("uuid", uuid4()),
    ("name", random_lower_string()),
    ("is_public", random_bool()),
    ("disk", random_non_negative_int()),
    ("ram", random_non_negative_int()),
    ("vcpus", random_non_negative_int()),
    ("swap", random_non_negative_int()),
    ("ephemeral", random_non_negative_int()),
    ("infiniband", random_bool()),
    ("gpus", random_positive_int()),
    ("local_storage", random_lower_string()),
    ("uuid", None),
    ("name", None),
    ("local_storage", None),
]
invalid_patch_key_values = [  # None is not accepted because there is a default
    ("description", None),
    ("is_public", None),
    ("disk", None),
    ("ram", None),
    ("vcpus", None),
    ("swap", None),
    ("ephemeral", None),
    ("infiniband", None),
    ("gpus", None),
    *gpu_details,
]


@fixture
@parametrize("k, v", patch_key_values)
def flavor_patch_valid_data_single_attr(k: str, v: Any) -> Dict[str, Any]:
    """Valid set of single key-value pair for a Flavor patch schema."""
    return {k: v}


@fixture
@parametrize("k, v", gpu_details)
def flavor_patch_valid_data_for_gpus(k: str, v: Any) -> Dict[str, Any]:
    """Valid set of attributes for a Flavor patch schema. GPU details."""
    return {"gpus": random_positive_int(), k: v}


@fixture
@parametrize("k, v", invalid_patch_key_values)
def flavor_patch_invalid_data(k: str, v: Any) -> Dict[str, Any]:
    """Invalid set of attributes for a Flavor patch schema."""
    return {k: v}


flavor_patch_valid_data = fixture_union(
    "flavor_patch_valid_data",
    (flavor_patch_valid_data_single_attr, flavor_patch_valid_data_for_gpus),
    idstyle="explicit",
)
