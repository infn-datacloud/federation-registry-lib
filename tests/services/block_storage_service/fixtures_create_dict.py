"""BlockStorageService specific fixtures."""
from typing import Any, Dict

from pytest_cases import fixture, fixture_union, parametrize

from app.provider.schemas_extended import (
    BlockStorageQuotaCreateExtended,
)
from app.service.enum import ServiceType
from tests.services.block_storage_service.utils import (
    random_block_storage_service_all_attr,
    random_block_storage_service_required_attr,
)

invalid_create_key_values = [
    ("description", None),
    ("type", None),
    ("type", ServiceType.COMPUTE),
    ("type", ServiceType.IDENTITY),
    ("type", ServiceType.NETWORK),
    ("endpoint", None),
    ("name", None),
]


@fixture
def block_storage_service_create_minimum_data() -> Dict[str, Any]:
    """Dict with BlockStorageService mandatory attributes."""
    return random_block_storage_service_required_attr()


@fixture
def block_storage_service_create_data_passing_empty_list() -> Dict[str, Any]:
    """Dict with all Region attributes.

    Passing an empty list is not a problem.
    """
    return {**random_block_storage_service_all_attr(), "quotas": []}


@fixture
def block_storage_service_create_data_with_quotas(
    block_storage_quota_create_data_with_rel: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with relationships attributes."""
    quota = BlockStorageQuotaCreateExtended(**block_storage_quota_create_data_with_rel)
    return {**random_block_storage_service_all_attr(), "quotas": [quota]}


@fixture
def block_storage_service_create_data_with_2_quotas_same_proj(
    block_storage_quota_create_data_with_rel: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with 2 quotas on same project.

    A quota has the flag 'per_user' equals to True and the other equal to False.
    """
    quota1 = BlockStorageQuotaCreateExtended(**block_storage_quota_create_data_with_rel)
    block_storage_quota_create_data_with_rel[
        "per_user"
    ] = not block_storage_quota_create_data_with_rel["per_user"]
    quota2 = BlockStorageQuotaCreateExtended(**block_storage_quota_create_data_with_rel)
    return {**random_block_storage_service_all_attr(), "quotas": [quota1, quota2]}


@fixture
@parametrize("k, v", invalid_create_key_values)
def block_storage_service_create_invalid_pair(k: str, v: Any) -> Dict[str, Any]:
    """Dict with one invalid key-value pair."""
    return {**random_block_storage_service_required_attr(), k: v}


@fixture
def block_storage_service_invalid_num_quotas_same_project(
    block_storage_quota_create_data_with_rel: Dict[str, Any],
) -> Dict[str, Any]:
    """Invalid number of quotas on same project.

    A project can have at most one `project` quota and one `per-user` quota on a
    specific service.
    """
    quota = BlockStorageQuotaCreateExtended(**block_storage_quota_create_data_with_rel)
    return {**random_block_storage_service_all_attr(), "quotas": [quota, quota]}


block_storage_service_create_valid_data = fixture_union(
    "block_storage_service_create_valid_data",
    (
        block_storage_service_create_minimum_data,
        block_storage_service_create_data_passing_empty_list,
        block_storage_service_create_data_with_quotas,
        block_storage_service_create_data_with_2_quotas_same_proj,
    ),
    idstyle="explicit",
)

block_storage_service_create_invalid_data = fixture_union(
    "block_storage_service_create_invalid_data",
    (
        block_storage_service_create_invalid_pair,
        block_storage_service_invalid_num_quotas_same_project,
    ),
    idstyle="explicit",
)
