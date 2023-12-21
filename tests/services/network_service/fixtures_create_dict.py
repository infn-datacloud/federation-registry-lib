"""NetworkService specific fixtures."""
from typing import Any, Dict

from pytest_cases import fixture, fixture_union, parametrize

from app.service.enum import ServiceType
from tests.network.utils import (
    IS_SHARED,
    random_network_required_attr,
    random_network_required_rel,
)
from tests.quotas.network_quota.utils import (
    random_network_quota_required_attr,
    random_network_quota_required_rel,
)
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
@parametrize(is_shared=IS_SHARED)
def network_service_create_data_with_networks(is_shared: bool) -> Dict[str, Any]:
    """Dict with relationships attributes."""
    return {
        **random_network_service_all_attr(),
        "networks": [
            {
                **random_network_required_attr(),
                **random_network_required_rel(is_shared),
                "is_shared": is_shared,
            }
        ],
    }


@fixture
def network_service_create_data_with_quotas() -> Dict[str, Any]:
    """Dict with relationships attributes."""
    return {
        **random_network_service_all_attr(),
        "quotas": [
            {
                **random_network_quota_required_attr(),
                **random_network_quota_required_rel(),
            }
        ],
    }


@fixture
def network_service_create_data_with_2_quotas_same_proj() -> Dict[str, Any]:
    """Dict with 2 quotas on same project.

    A quota has the flag 'per_user' equals to True and the other equal to False.
    """
    quota1 = {
        **random_network_quota_required_attr(),
        **random_network_quota_required_rel(),
        "per_user": False,
    }
    quota2 = {
        **random_network_quota_required_attr(),
        **random_network_quota_required_rel(),
        "per_user": True,
    }
    return {**random_network_service_all_attr(), "quotas": [quota1, quota2]}


@fixture
@parametrize("k, v", invalid_create_key_values)
def network_service_create_invalid_pair(k: str, v: Any) -> Dict[str, Any]:
    """Dict with one invalid key-value pair."""
    return {**random_network_service_required_attr(), k: v}


@fixture
def network_service_invalid_num_quotas_same_project() -> Dict[str, Any]:
    """Invalid number of quotas on same project.

    A project can have at most one `project` quota and one `per-user` quota on a
    specific service.
    """
    quota = {
        **random_network_quota_required_attr(),
        **random_network_quota_required_rel(),
    }
    return {**random_network_service_required_attr(), "quotas": [quota, quota]}


@fixture
def network_service_create_duplicate_networks() -> Dict[str, Any]:
    """Invalid case: the network list has duplicate values."""
    network = random_network_required_attr()
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
