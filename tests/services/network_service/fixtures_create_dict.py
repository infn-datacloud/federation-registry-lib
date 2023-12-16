"""NetworkService specific fixtures."""
from typing import Any, Dict

from pytest_cases import fixture, fixture_union, parametrize

from app.provider.schemas_extended import (
    NetworkCreateExtended,
    NetworkQuotaCreateExtended,
)
from app.service.enum import ServiceType
from tests.common.utils import random_lower_string, random_url
from tests.services.utils import random_network_service_name

invalid_create_key_values = [
    ("description", None),
    ("type", None),
    ("type", ServiceType.BLOCK_STORAGE),
    ("type", ServiceType.COMPUTE),
    ("type", ServiceType.IDENTITY),
    ("endpoint", None),
    ("name", None),
]
relationships_attr = ["networks", "quotas"]


@fixture
def network_service_create_mandatory_data() -> Dict[str, Any]:
    """Dict with NetworkService mandatory attributes."""
    return {"endpoint": random_url(), "name": random_network_service_name()}


@fixture
def network_service_create_all_data(
    network_service_create_mandatory_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with all NetworkService attributes.

    Attribute is_public has been parametrized.
    """
    return {
        **network_service_create_mandatory_data,
        "description": random_lower_string(),
    }


@fixture
@parametrize(attr=relationships_attr)
def network_service_create_data_passing_empty_list(
    attr: str, network_service_create_all_data: Dict[str, Any]
) -> Dict[str, Any]:
    """Dict with all Region attributes.

    Passing an empty list is not a problem.
    """
    return {**network_service_create_all_data, attr: []}


@fixture
def network_service_create_data_with_networks(
    network_service_create_all_data: Dict[str, Any],
    network_create_data_with_rel: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with relationships attributes."""
    network = NetworkCreateExtended(**network_create_data_with_rel)
    return {**network_service_create_all_data, "networks": [network]}


@fixture
def network_service_create_data_with_quotas(
    network_service_create_all_data: Dict[str, Any],
    network_quota_create_data_with_rel: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with relationships attributes."""
    quota = NetworkQuotaCreateExtended(**network_quota_create_data_with_rel)
    return {**network_service_create_all_data, "quotas": [quota]}


@fixture
def network_service_create_data_with_2_quotas_same_proj(
    network_service_create_all_data: Dict[str, Any],
    network_quota_create_data_with_rel: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with 2 quotas on same project.

    A quota has the flag 'per_user' equals to True and the other equal to False.
    """
    quota1 = NetworkQuotaCreateExtended(**network_quota_create_data_with_rel)
    network_quota_create_data_with_rel[
        "per_user"
    ] = not network_quota_create_data_with_rel["per_user"]
    quota2 = NetworkQuotaCreateExtended(**network_quota_create_data_with_rel)
    return {**network_service_create_all_data, "quotas": [quota1, quota2]}


@fixture
@parametrize("k, v", invalid_create_key_values)
def network_service_create_invalid_pair(
    network_service_create_mandatory_data: Dict[str, Any], k: str, v: Any
) -> Dict[str, Any]:
    """Dict with one invalid key-value pair."""
    data = {**network_service_create_mandatory_data}
    data[k] = v
    return data


@fixture
def network_service_invalid_num_quotas_same_project(
    network_service_create_mandatory_data: Dict[str, Any],
    network_quota_create_data_with_rel: Dict[str, Any],
) -> Dict[str, Any]:
    """Invalid number of quotas on same project.

    A project can have at most one `project` quota and one `per-user` quota on a
    specific service.
    """
    quota = NetworkQuotaCreateExtended(**network_quota_create_data_with_rel)
    return {**network_service_create_mandatory_data, "quotas": [quota, quota]}


@fixture
def network_service_create_duplicate_networks(
    network_service_create_mandatory_data: Dict[str, Any],
    network_create_mandatory_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Invalid case: the network list has duplicate values."""
    network = NetworkCreateExtended(**network_create_mandatory_data)
    return {**network_service_create_mandatory_data, "networks": [network, network]}


network_service_create_valid_data = fixture_union(
    "network_service_create_valid_data",
    (
        network_service_create_mandatory_data,
        network_service_create_data_with_networks,
        network_service_create_data_with_quotas,
        network_service_create_data_with_2_quotas_same_proj,
    ),
    idstyle="explicit",
)

network_service_create_invalid_data = fixture_union(
    "network_service_create_invalid_data",
    (
        network_service_create_invalid_pair,
        network_service_invalid_num_quotas_same_project,
        network_service_create_duplicate_networks,
    ),
    idstyle="explicit",
)
