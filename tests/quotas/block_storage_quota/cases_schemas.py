"""BlockStorageQuota specific cases."""
from typing import Any, Dict, Tuple, Type, Union

from pytest_cases import case, parametrize

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


@case(tags="create_valid")
def case_block_storage_quota_create_valid_schema_actors(
    block_storage_quota_create_valid_data: Dict[str, Any],
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


@case(tags="create_invalid")
def case_block_storage_quota_create_invalid_schema_actors(
    block_storage_quota_create_invalid_data: Dict[str, Any],
) -> Tuple[Type[BlockStorageQuotaCreateExtended], Dict[str, Any]]:
    """Fixture with the create class and the invalid data to validate."""
    return BlockStorageQuotaCreateExtended, block_storage_quota_create_invalid_data


@case(tags="patch_valid")
def case_block_storage_quota_patch_valid_schema_actors(
    block_storage_quota_patch_valid_data: Dict[str, Any],
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


@case(tags="patch_invalid")
def case_block_storage_quota_patch_invalid_schema_actors(
    block_storage_quota_patch_invalid_data: Dict[str, Any],
) -> Tuple[Type[BlockStorageQuotaUpdate], Dict[str, Any]]:
    """Fixture with the update class and the invalid data to validate."""
    return BlockStorageQuotaUpdate, block_storage_quota_patch_invalid_data


@case(tags="read")
@parametrize(
    cls=[
        BlockStorageQuotaRead,
        BlockStorageQuotaReadExtended,
        BlockStorageQuotaReadPublic,
        BlockStorageQuotaReadExtendedPublic,
    ],
)
def case_block_storage_quota_valid_read_schema_tuple(
    cls: Union[
        BlockStorageQuotaRead,
        BlockStorageQuotaReadPublic,
        BlockStorageQuotaReadExtended,
        BlockStorageQuotaReadExtendedPublic,
    ],
    db_block_storage_quota: BlockStorageQuota,
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
    bool,
    bool,
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
    cls_name = cls.__name__
    is_public = False
    is_extended = False
    if "Public" in cls_name:
        is_public = True
    if "Extended" in cls_name:
        is_extended = True
    return cls, validator, db_block_storage_quota, is_public, is_extended
