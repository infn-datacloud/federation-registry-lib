"""BlockStorageQuota specific fixtures."""
from typing import Any, Dict, Tuple, Type, Union
from uuid import uuid4

import pytest
from pytest_cases import fixture, fixture_ref, parametrize

from app.provider.models import Provider
from app.provider.schemas_extended import BlockStorageQuotaCreateExtended
from app.quota.crud import block_storage_quota_mng
from app.quota.enum import QuotaType
from app.quota.models import BlockStorageQuota
from app.quota.schemas import (
    BlockStorageQuotaBase,
    BlockStorageQuotaRead,
    BlockStorageQuotaReadPublic,
    BlockStorageQuotaUpdate,
    QuotaBase,
)
from app.quota.schemas_extended import (
    BlockStorageQuotaReadExtended,
    BlockStorageQuotaReadExtendedPublic,
)
from app.region.models import Region
from app.service.models import BlockStorageService
from tests.common.schema_validators import (
    BaseSchemaValidation,
    CreateSchemaValidation,
    ReadSchemaValidation,
)
from tests.utils.utils import random_bool, random_lower_string, random_non_negative_int

invalid_create_key_values = {
    ("description", None),
    ("per_user", None),
    ("gigabytes", -2),  # -1 is valid
    ("per_volume_gigabytes", -2),  # -1 is valid
    ("volumes", -2),  # -1 is valid
}
patch_key_values = {
    ("description", random_lower_string()),
    ("per_user", random_bool()),
    ("gigabytes", random_non_negative_int()),
    ("gigabytes", -1),
    ("per_volume_gigabytes", random_non_negative_int()),
    ("per_volume_gigabytes", -1),
    ("volumes", random_non_negative_int()),
    ("volumes", -1),
}
invalid_patch_key_values = {  # None is not accepted because there is a default
    ("description", None),
    ("per_user", None),
    ("type", QuotaType.COMPUTE),
    ("type", QuotaType.NETWORK),
    ("gigabytes", -2),  # -1 is valid
    ("per_volume_gigabytes", -2),  # -1 is valid
    ("volumes", -2),  # -1 is valid
}
per_user = {True, False}


# CLASSES FIXTURES


@fixture(scope="package")
def block_storage_quota_create_validator() -> (
    CreateSchemaValidation[
        BlockStorageQuotaBase, QuotaBase, BlockStorageQuotaCreateExtended
    ]
):
    """Instance to validate block_storage_quota create schemas."""
    return CreateSchemaValidation[
        BlockStorageQuotaBase, QuotaBase, BlockStorageQuotaCreateExtended
    ](
        base=BlockStorageQuotaBase,
        base_public=QuotaBase,
        create=BlockStorageQuotaCreateExtended,
    )


@fixture(scope="package")
def block_storage_quota_read_validator() -> (
    ReadSchemaValidation[
        BlockStorageQuotaBase,
        QuotaBase,
        BlockStorageQuotaRead,
        BlockStorageQuotaReadPublic,
        BlockStorageQuotaReadExtended,
        BlockStorageQuotaReadExtendedPublic,
        BlockStorageQuota,
    ]
):
    """Instance to validate block_storage_quota read schemas."""
    return ReadSchemaValidation[
        BlockStorageQuotaBase,
        QuotaBase,
        BlockStorageQuotaRead,
        BlockStorageQuotaReadPublic,
        BlockStorageQuotaReadExtended,
        BlockStorageQuotaReadExtendedPublic,
        BlockStorageQuota,
    ](
        base=BlockStorageQuotaBase,
        base_public=QuotaBase,
        read=BlockStorageQuotaRead,
        read_extended=BlockStorageQuotaReadExtended,
    )


@fixture(scope="package")
def block_storage_quota_patch_validator() -> (
    BaseSchemaValidation[BlockStorageQuotaBase, QuotaBase]
):
    """Instance to validate block_storage_quota patch schemas."""
    return BaseSchemaValidation[BlockStorageQuotaBase, QuotaBase](
        base=BlockStorageQuotaBase, base_public=QuotaBase
    )


@fixture(scope="package")
@parametrize(
    "cls",
    {
        BlockStorageQuotaRead,
        BlockStorageQuotaReadExtended,
        BlockStorageQuotaReadPublic,
        BlockStorageQuotaReadExtendedPublic,
    },
)
def block_storage_quota_read_class(cls) -> Any:
    """BlockStorageQuota Read schema."""
    return cls


# DICT FIXTURES CREATE


@fixture
def block_storage_quota_create_mandatory_data() -> Dict[str, Any]:
    """Dict with BlockStorageQuota mandatory attributes."""
    return {}


@fixture
def block_storage_quota_create_all_data(
    block_storage_quota_create_mandatory_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with all BlockStorageQuota attributes."""
    return {
        **block_storage_quota_create_mandatory_data,
        "description": random_lower_string(),
        "per_user": random_bool(),
        "gigabytes": random_non_negative_int(),
        "per_volume_gigabytes": random_non_negative_int(),
        "volumes": random_non_negative_int(),
    }


@fixture
def block_storage_quota_create_data_with_rel(
    block_storage_quota_create_all_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with relationships attributes."""
    return {**block_storage_quota_create_all_data, "project": uuid4()}


@fixture
@parametrize("data", {fixture_ref("block_storage_quota_create_data_with_rel")})
def block_storage_quota_create_valid_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Valid set of attributes for a BlockStorageQuota patch schema."""
    return data


@fixture
@parametrize("k, v", invalid_create_key_values)
def block_storage_quota_create_invalid_pair(
    block_storage_quota_create_data_with_rel: Dict[str, Any], k: str, v: Any
) -> Dict[str, Any]:
    """Dict with one invalid key-value pair."""
    data = {**block_storage_quota_create_data_with_rel}
    data[k] = v
    return data


@fixture
@parametrize(
    "data",
    {
        fixture_ref("block_storage_quota_create_invalid_pair"),
        fixture_ref("block_storage_quota_create_mandatory_data"),
    },
)
def block_storage_quota_create_invalid_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Invalid set of attributes for a BlockStorageQuota create schema."""
    return data


# DICT FIXTURES PATCH


@fixture
@parametrize("k, v", patch_key_values)
def block_storage_quota_patch_valid_data_single_attr(k: str, v: Any) -> Dict[str, Any]:
    """Valid set of single key-value pair for a BlockStorageQuota patch schema."""
    return {k: v}


@fixture
@parametrize("data", {fixture_ref("block_storage_quota_patch_valid_data_single_attr")})
def block_storage_quota_patch_valid_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Valid set of attributes for a BlockStorageQuota patch schema."""
    return data


@fixture
@parametrize("k, v", invalid_patch_key_values)
def block_storage_quota_patch_invalid_data(k: str, v: Any) -> Dict[str, Any]:
    """Invalid set of attributes for a BlockStorageQuota patch schema."""
    return {k: v}


# DB INSTANCES FIXTURES


@fixture
@parametrize(per_user=per_user)
def db_block_storage_quota_simple(
    per_user: bool,
    block_storage_quota_create_mandatory_data: Dict[str, Any],
    db_block_storage_service_simple: BlockStorageService,
) -> BlockStorageQuota:
    """Fixture with standard DB BlockStorageQuota."""
    db_region: Region = db_block_storage_service_simple.region.single()
    db_provider: Provider = db_region.provider.single()
    projects = [i.uuid for i in db_provider.projects]
    if len(projects) == 1:
        pytest.skip("Case with only one project in the provider already considered.")

    item = BlockStorageQuotaCreateExtended(
        **block_storage_quota_create_mandatory_data,
        per_user=per_user,
        project=projects[0],
    )
    return block_storage_quota_mng.create(
        obj_in=item,
        service=db_block_storage_service_simple,
        project=db_provider.projects.single(),
    )


@fixture
@parametrize("db_item", {fixture_ref("db_block_storage_quota_simple")})
def db_block_storage_quota(db_item: BlockStorageQuota) -> BlockStorageQuota:
    """Generic DB BlockStorageQuota instance."""
    return db_item


# TUPLE FOR CASES FIXTURES


@fixture
def block_storage_quota_valid_create_schema_tuple(
    block_storage_quota_create_validator, block_storage_quota_create_valid_data
) -> Tuple[
    Type[BlockStorageQuotaCreateExtended],
    CreateSchemaValidation[
        BlockStorageQuotaBase, QuotaBase, BlockStorageQuotaCreateExtended
    ],
    Dict[str, Any],
]:
    """Fixture with the create class, validator and data to validate."""
    return (
        BlockStorageQuotaCreateExtended,
        block_storage_quota_create_validator,
        block_storage_quota_create_valid_data,
    )


@fixture
def block_storage_quota_invalid_create_schema_tuple(
    block_storage_quota_create_invalid_data,
) -> Tuple[Type[BlockStorageQuotaCreateExtended], Dict[str, Any]]:
    """Fixture with the create class and the invalid data to validate."""
    return BlockStorageQuotaCreateExtended, block_storage_quota_create_invalid_data


@fixture
def block_storage_quota_valid_patch_schema_tuple(
    block_storage_quota_patch_validator, block_storage_quota_patch_valid_data
) -> Tuple[
    Type[BlockStorageQuotaUpdate],
    BaseSchemaValidation[BlockStorageQuotaBase, QuotaBase],
    Dict[str, Any],
]:
    """Fixture with the update class, validator and data to validate."""
    return (
        BlockStorageQuotaUpdate,
        block_storage_quota_patch_validator,
        block_storage_quota_patch_valid_data,
    )


@fixture
def block_storage_quota_invalid_patch_schema_tuple(
    block_storage_quota_patch_invalid_data,
) -> Tuple[Type[BlockStorageQuotaUpdate], Dict[str, Any]]:
    """Fixture with the update class and the invalid data to validate."""
    return BlockStorageQuotaUpdate, block_storage_quota_patch_invalid_data


@fixture
def block_storage_quota_valid_read_schema_tuple(
    block_storage_quota_read_class,
    block_storage_quota_read_validator,
    db_block_storage_quota,
) -> Tuple[
    Union[
        BlockStorageQuotaRead,
        BlockStorageQuotaReadPublic,
        BlockStorageQuotaReadExtended,
        BlockStorageQuotaReadExtendedPublic,
    ],
    ReadSchemaValidation[
        BlockStorageQuotaBase,
        QuotaBase,
        BlockStorageQuotaRead,
        BlockStorageQuotaReadPublic,
        BlockStorageQuotaReadExtended,
        BlockStorageQuotaReadExtendedPublic,
        BlockStorageQuota,
    ],
    BlockStorageQuota,
]:
    """Fixture with the read class, validator and the db item to read."""
    return (
        block_storage_quota_read_class,
        block_storage_quota_read_validator,
        db_block_storage_quota,
    )
