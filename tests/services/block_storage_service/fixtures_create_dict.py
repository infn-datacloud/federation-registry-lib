"""BlockStorageService specific fixtures."""
from typing import Any, Dict

from pytest_cases import fixture, fixture_union, parametrize

from app.provider.schemas_extended import (
    BlockStorageQuotaCreateExtended,
)
from app.service.enum import ServiceType
from tests.utils.block_storage_service import random_block_storage_service_name
from tests.utils.utils import random_lower_string, random_url

invalid_create_key_values = [
    ("description", None),
    ("type", None),
    ("type", ServiceType.COMPUTE),
    ("type", ServiceType.IDENTITY),
    ("type", ServiceType.NETWORK),
    ("endpoint", None),
    ("name", None),
]
relationships_attr = ["quotas"]


@fixture
def block_storage_service_create_mandatory_data() -> Dict[str, Any]:
    """Dict with BlockStorageService mandatory attributes."""
    return {"endpoint": random_url(), "name": random_block_storage_service_name()}


@fixture
def block_storage_service_create_all_data(
    block_storage_service_create_mandatory_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with all BlockStorageService attributes."""
    return {
        **block_storage_service_create_mandatory_data,
        "description": random_lower_string(),
    }


@fixture
@parametrize(attr=relationships_attr)
def block_storage_service_create_data_passing_empty_list(
    attr: str, block_storage_service_create_all_data: Dict[str, Any]
) -> Dict[str, Any]:
    """Dict with all Region attributes.

    Passing an empty list is not a problem.
    """
    return {**block_storage_service_create_all_data, attr: []}


@fixture
def block_storage_service_create_data_with_quotas(
    block_storage_service_create_all_data: Dict[str, Any],
    block_storage_quota_create_data_with_rel: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with relationships attributes."""
    quota = BlockStorageQuotaCreateExtended(**block_storage_quota_create_data_with_rel)
    return {**block_storage_service_create_all_data, "quotas": [quota]}


@fixture
def block_storage_service_create_data_with_2_quotas_same_proj(
    block_storage_service_create_all_data: Dict[str, Any],
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
    return {**block_storage_service_create_all_data, "quotas": [quota1, quota2]}


@fixture
@parametrize("k, v", invalid_create_key_values)
def block_storage_service_create_invalid_pair(
    block_storage_service_create_mandatory_data: Dict[str, Any], k: str, v: Any
) -> Dict[str, Any]:
    """Dict with one invalid key-value pair."""
    data = {**block_storage_service_create_mandatory_data}
    data[k] = v
    return data


@fixture
def block_storage_service_invalid_num_quotas_same_project(
    block_storage_service_create_mandatory_data: Dict[str, Any],
    block_storage_quota_create_data_with_rel: Dict[str, Any],
) -> Dict[str, Any]:
    """Invalid number of quotas on same project.

    A project can have at most one `project` quota and one `per-user` quota on a
    specific service.
    """
    quota = BlockStorageQuotaCreateExtended(**block_storage_quota_create_data_with_rel)
    return {**block_storage_service_create_mandatory_data, "quotas": [quota, quota]}


block_storage_service_create_valid_data = fixture_union(
    "block_storage_service_create_valid_data",
    (
        block_storage_service_create_mandatory_data,
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
