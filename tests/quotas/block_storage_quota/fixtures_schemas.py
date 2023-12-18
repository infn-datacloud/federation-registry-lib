"""BlockStorageQuota specific fixtures."""
from typing import Any, Dict, Tuple, Type, Union

from pytest_cases import fixture, parametrize

from app.provider.schemas_extended import (
    BlockStorageQuotaCreateExtended,
)
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
from tests.common.schemas.validators import (
    CreateSchemaValidation,
    PatchSchemaValidation,
    ReadSchemaValidation,
)


@fixture
@parametrize(
    cls=[
        BlockStorageQuotaRead,
        BlockStorageQuotaReadExtended,
        BlockStorageQuotaReadPublic,
        BlockStorageQuotaReadExtendedPublic,
    ],
)
def block_storage_quota_read_class(cls) -> Any:
    """BlockStorageQuota Read schema."""
    return cls


@fixture
def block_storage_quota_valid_create_schema_tuple(
    block_storage_quota_create_valid_data,
) -> Tuple[
    Type[BlockStorageQuotaCreateExtended],
    CreateSchemaValidation[
        BlockStorageQuotaBase, QuotaBase, BlockStorageQuotaCreateExtended
    ],
    Dict[str, Any],
]:
    """Fixture with the create class, validator and data to validate."""
    validator = CreateSchemaValidation[
        BlockStorageQuotaBase,
        QuotaBase,
        BlockStorageQuotaCreateExtended,
    ](
        base=BlockStorageQuotaBase,
        base_public=QuotaBase,
        create=BlockStorageQuotaCreateExtended,
    )
    return (
        BlockStorageQuotaCreateExtended,
        validator,
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
    block_storage_quota_patch_valid_data,
) -> Tuple[
    Type[BlockStorageQuotaUpdate],
    PatchSchemaValidation[BlockStorageQuotaBase, QuotaBase],
    Dict[str, Any],
]:
    """Fixture with the update class, validator and data to validate."""
    validator = PatchSchemaValidation[BlockStorageQuotaBase, QuotaBase](
        base=BlockStorageQuotaBase, base_public=QuotaBase
    )
    return BlockStorageQuotaUpdate, validator, block_storage_quota_patch_valid_data


@fixture
def block_storage_quota_invalid_patch_schema_tuple(
    block_storage_quota_patch_invalid_data,
) -> Tuple[Type[BlockStorageQuotaUpdate], Dict[str, Any]]:
    """Fixture with the update class and the invalid data to validate."""
    return BlockStorageQuotaUpdate, block_storage_quota_patch_invalid_data


@fixture
def block_storage_quota_valid_read_schema_tuple(
    block_storage_quota_read_class,
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
    validator = ReadSchemaValidation[
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
    return block_storage_quota_read_class, validator, db_block_storage_quota
