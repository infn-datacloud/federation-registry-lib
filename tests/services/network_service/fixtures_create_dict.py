"""NetworkService specific fixtures."""
from typing import Any, Dict

from pytest_cases import fixture, fixture_union, parametrize

from app.provider.schemas_extended import (
    NetworkCreateExtended,
    NetworkQuotaCreateExtended,
)
from app.service.enum import ServiceType
from tests.network.utils import random_network_required_attr
from tests.services.network_service.utils import (
    random_network_service_all_attr,
    random_network_service_required_attr,
)

invalid_create_key_values = [
    ("description", None),
    ("type", None),
    ("type", ServiceType.BLOCK_STORAGE),
    ("type", ServiceType.COMPUTE),
    ("type", ServiceType.IDENTITY),
    ("endpoint", None),
    ("name", None),
]


@fixture
def network_service_create_minimum_data() -> Dict[str, Any]:
    """Dict with NetworkService mandatory attributes."""
    return random_network_service_required_attr()


@fixture
@parametrize(attr=["networks", "quotas"])
def network_service_create_data_passing_empty_list(attr: str) -> Dict[str, Any]:
    """Dict with all Region attributes.

    Passing an empty list is not a problem.
    """
    return {**random_network_service_all_attr(), attr: []}


@fixture
def network_service_create_data_with_networks(
    network_create_data_with_rel: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with relationships attributes."""
    network = NetworkCreateExtended(**network_create_data_with_rel)
    return {**random_network_service_all_attr(), "networks": [network]}


@fixture
def network_service_create_data_with_quotas(
    network_quota_create_data_with_rel: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with relationships attributes."""
    quota = NetworkQuotaCreateExtended(**network_quota_create_data_with_rel)
    return {**random_network_service_all_attr(), "quotas": [quota]}


@fixture
def network_service_create_data_with_2_quotas_same_proj(
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
    return {**random_network_service_all_attr(), "quotas": [quota1, quota2]}


@fixture
@parametrize("k, v", invalid_create_key_values)
def network_service_create_invalid_pair(k: str, v: Any) -> Dict[str, Any]:
    """Dict with one invalid key-value pair."""
    return {**random_network_service_required_attr(), k: v}


@fixture
def network_service_invalid_num_quotas_same_project(
    network_quota_create_data_with_rel: Dict[str, Any],
) -> Dict[str, Any]:
    """Invalid number of quotas on same project.

    A project can have at most one `project` quota and one `per-user` quota on a
    specific service.
    """
    quota = NetworkQuotaCreateExtended(**network_quota_create_data_with_rel)
    return {**random_network_service_required_attr(), "quotas": [quota, quota]}


@fixture
def network_service_create_duplicate_networks() -> Dict[str, Any]:
    """Invalid case: the network list has duplicate values."""
    network = NetworkCreateExtended(**random_network_required_attr())
    return {**random_network_service_required_attr(), "networks": [network, network]}


network_service_create_valid_data = fixture_union(
    "network_service_create_valid_data",
    (
        network_service_create_minimum_data,
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
