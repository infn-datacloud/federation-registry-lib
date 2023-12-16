"""Region specific fixtures."""
from typing import Any, Dict

from pytest_cases import fixture, fixture_union, parametrize

from app.provider.schemas_extended import (
    BlockStorageServiceCreateExtended,
    ComputeServiceCreateExtended,
    IdentityServiceCreate,
    LocationCreate,
    NetworkServiceCreateExtended,
)
from tests.utils.block_storage_service import random_block_storage_service_name
from tests.utils.compute_service import random_compute_service_name
from tests.utils.identity_service import random_identity_service_name
from tests.utils.network_service import random_network_service_name
from tests.utils.utils import random_lower_string, random_url

invalid_create_key_values = [("description", None), ("name", None)]
relationships_num = [1, 2]
relationships_attr = [
    "block_storage_services",
    "compute_services",
    "identity_services",
    "network_services",
]


@fixture
def region_create_mandatory_data() -> Dict[str, Any]:
    """Dict with Region mandatory attributes."""
    return {"name": random_lower_string()}


@fixture
def region_create_all_data(
    region_create_mandatory_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with Region mandatory attributes."""
    return {**region_create_mandatory_data, "description": random_lower_string()}


@fixture
@parametrize(attr=relationships_attr)
def region_create_data_passing_empty_list(
    attr: str, region_create_all_data: Dict[str, Any]
) -> Dict[str, Any]:
    """Dict with all Region attributes.

    Passing an empty list is not a problem.
    """
    return {**region_create_all_data, attr: []}


@fixture
def region_create_data_with_location(
    region_create_all_data: Dict[str, Any],
    location_create_mandatory_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with relationships attributes."""
    location = LocationCreate(**location_create_mandatory_data)
    return {**region_create_all_data, "location": location}


@fixture
@parametrize(owned_services=relationships_num)
def region_create_data_with_block_storage_services(
    owned_services: int,
    region_create_all_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with relationships attributes."""
    services = []
    for _ in range(owned_services):
        services.append(
            BlockStorageServiceCreateExtended(
                endpoint=random_url(), name=random_block_storage_service_name()
            )
        )
    return {**region_create_all_data, "block_storage_services": services}


@fixture
def region_create_data_with_single_compute_service(
    region_create_all_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with relationships attributes."""
    return {
        **region_create_all_data,
        "compute_services": [
            ComputeServiceCreateExtended(
                endpoint=random_url(), name=random_compute_service_name()
            )
        ],
    }


@fixture
def region_create_data_with_compute_services(
    region_create_all_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with relationships attributes."""
    return {
        **region_create_all_data,
        "compute_services": [
            ComputeServiceCreateExtended(
                endpoint=random_url(), name=random_compute_service_name()
            ),
            ComputeServiceCreateExtended(
                endpoint=random_url(), name=random_compute_service_name()
            ),
        ],
    }


@fixture
@parametrize(owned_services=relationships_num)
def region_create_data_with_identity_services(
    owned_services: int,
    region_create_all_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with relationships attributes."""
    services = []
    for _ in range(owned_services):
        services.append(
            IdentityServiceCreate(
                endpoint=random_url(), name=random_identity_service_name()
            )
        )
    return {**region_create_all_data, "identity_services": services}


@fixture
@parametrize(owned_services=relationships_num)
def region_create_data_with_network_services(
    owned_services: int,
    region_create_all_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with relationships attributes."""
    services = []
    for _ in range(owned_services):
        services.append(
            NetworkServiceCreateExtended(
                endpoint=random_url(), name=random_network_service_name()
            )
        )
    return {**region_create_all_data, "network_services": services}


@fixture
@parametrize("k, v", invalid_create_key_values)
def region_create_invalid_pair(
    region_create_mandatory_data: Dict[str, Any], k: str, v: Any
) -> Dict[str, Any]:
    """Dict with one invalid key-value pair."""
    data = {**region_create_mandatory_data}
    data[k] = v
    return data


@fixture
def region_create_duplicate_block_storage_services(
    region_create_mandatory_data: Dict[str, Any],
    block_storage_service_create_mandatory_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Invalid case: the project list has duplicate values."""
    service = BlockStorageServiceCreateExtended(
        **block_storage_service_create_mandatory_data
    )
    return {
        **region_create_mandatory_data,
        "block_storage_services": [service, service],
    }


@fixture
def region_create_duplicate_compute_services(
    region_create_mandatory_data: Dict[str, Any],
    compute_service_create_mandatory_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Invalid case: the project list has duplicate values."""
    service = ComputeServiceCreateExtended(**compute_service_create_mandatory_data)
    return {**region_create_mandatory_data, "compute_services": [service, service]}


@fixture
def region_create_duplicate_identity_services(
    region_create_mandatory_data: Dict[str, Any],
    identity_service_create_mandatory_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Invalid case: the project list has duplicate values."""
    service = IdentityServiceCreate(**identity_service_create_mandatory_data)
    return {**region_create_mandatory_data, "identity_services": [service, service]}


@fixture
def region_create_duplicate_network_services(
    region_create_mandatory_data: Dict[str, Any],
    network_service_create_mandatory_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Invalid case: the project list has duplicate values."""
    service = NetworkServiceCreateExtended(**network_service_create_mandatory_data)
    return {**region_create_mandatory_data, "network_services": [service, service]}


region_create_valid_data = fixture_union(
    "region_create_valid_data",
    (
        region_create_mandatory_data,
        region_create_data_passing_empty_list,
        region_create_data_with_location,
        region_create_data_with_block_storage_services,
        region_create_data_with_single_compute_service,
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
