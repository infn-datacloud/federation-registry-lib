"""Region specific fixtures."""
from typing import Any, Dict

from pytest_cases import fixture, fixture_union, parametrize

from tests.location.utils import random_location_required_attr
from tests.region.utils import random_region_all_attr, random_region_required_attr
from tests.services.block_storage_service.utils import (
    random_block_storage_service_required_attr,
)
from tests.services.compute_service.utils import random_compute_service_required_attr
from tests.services.identity_service.utils import random_identity_service_required_attr
from tests.services.network_service.utils import random_network_service_required_attr

invalid_create_key_values = [("description", None), ("name", None)]
relationships_num = [1, 2]


@fixture
def region_create_minimum_data() -> Dict[str, Any]:
    """Dict with Region mandatory attributes."""
    return random_region_required_attr()


@fixture
@parametrize(
    attr=[
        "block_storage_services",
        "compute_services",
        "identity_services",
        "network_services",
    ]
)
def region_create_data_passing_empty_list(attr: str) -> Dict[str, Any]:
    """Dict with all Region attributes.

    Passing an empty list is not a problem.
    """
    return {**random_region_all_attr(), attr: []}


@fixture
def region_create_data_with_location() -> Dict[str, Any]:
    """Dict with relationships attributes."""
    return {
        **random_region_all_attr(),
        "location": random_location_required_attr(),
    }


@fixture
def region_create_data_with_block_storage_services() -> Dict[str, Any]:
    """Dict with relationships attributes."""
    return {
        **random_region_all_attr(),
        "block_storage_services": [random_block_storage_service_required_attr()],
    }


@fixture
def region_create_data_with_compute_services() -> Dict[str, Any]:
    """Dict with relationships attributes."""
    return {
        **random_region_all_attr(),
        "compute_services": [random_compute_service_required_attr()],
    }


@fixture
def region_create_data_with_identity_services() -> Dict[str, Any]:
    """Dict with relationships attributes."""
    return {
        **random_region_all_attr(),
        "identity_services": [random_identity_service_required_attr()],
    }


@fixture
def region_create_data_with_network_services() -> Dict[str, Any]:
    """Dict with relationships attributes."""
    return {
        **random_region_all_attr(),
        "network_services": [random_network_service_required_attr()],
    }


@fixture
@parametrize("k, v", invalid_create_key_values)
def region_create_invalid_pair(k: str, v: Any) -> Dict[str, Any]:
    """Dict with one invalid key-value pair."""
    return {**random_region_required_attr(), k: v}


@fixture
def region_create_duplicate_block_storage_services() -> Dict[str, Any]:
    """Invalid case: the project list has duplicate values."""
    service = random_block_storage_service_required_attr()
    return {
        **random_region_required_attr(),
        "block_storage_services": [service, service],
    }


@fixture
def region_create_duplicate_compute_services() -> Dict[str, Any]:
    """Invalid case: the project list has duplicate values."""
    service = random_compute_service_required_attr()
    return {**random_region_required_attr(), "compute_services": [service, service]}


@fixture
def region_create_duplicate_identity_services() -> Dict[str, Any]:
    """Invalid case: the project list has duplicate values."""
    service = random_identity_service_required_attr()
    return {**random_region_required_attr(), "identity_services": [service, service]}


@fixture
def region_create_duplicate_network_services() -> Dict[str, Any]:
    """Invalid case: the project list has duplicate values."""
    service = random_network_service_required_attr()
    return {**random_region_required_attr(), "network_services": [service, service]}


region_create_valid_data = fixture_union(
    "region_create_valid_data",
    (
        region_create_minimum_data,
        region_create_data_passing_empty_list,
        region_create_data_with_location,
        region_create_data_with_block_storage_services,
        region_create_data_with_compute_services,
        region_create_data_with_identity_services,
        region_create_data_with_network_services,
    ),
    idstyle="explicit",
)


region_create_invalid_data = fixture_union(
    "region_create_invalid_data",
    (
        region_create_invalid_pair,
        region_create_duplicate_block_storage_services,
        region_create_duplicate_compute_services,
        region_create_duplicate_identity_services,
        region_create_duplicate_network_services,
    ),
    idstyle="explicit",
)
