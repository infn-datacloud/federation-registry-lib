"""BlockStorageQuota specific fixtures."""
from typing import Any

from pytest_cases import fixture, parametrize

from app.provider.schemas_extended import (
    BlockStorageQuotaCreateExtended,
)
from app.quota.models import BlockStorageQuota
from app.quota.schemas import (
    BlockStorageQuotaBase,
    BlockStorageQuotaRead,
    BlockStorageQuotaReadPublic,
    QuotaBase,
)
from app.quota.schemas_extended import (
    BlockStorageQuotaReadExtended,
    BlockStorageQuotaReadExtendedPublic,
)
from tests.common.schema_validators import (
    BaseSchemaValidation,
    CreateSchemaValidation,
    ReadSchemaValidation,
)


@fixture
def block_storage_quota_create_validator() -> (
    CreateSchemaValidation[
        BlockStorageQuotaBase,
        QuotaBase,
        BlockStorageQuotaCreateExtended,
    ]
):
    """Instance to validate block_storage_quota create schemas."""
    return CreateSchemaValidation[
        BlockStorageQuotaBase,
        QuotaBase,
        BlockStorageQuotaCreateExtended,
    ](
        base=BlockStorageQuotaBase,
        base_public=QuotaBase,
        create=BlockStorageQuotaCreateExtended,
    )


@fixture
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


@fixture
def block_storage_quota_patch_validator() -> (
    BaseSchemaValidation[BlockStorageQuotaBase, QuotaBase]
):
    """Instance to validate block_storage_quota patch schemas."""
    return BaseSchemaValidation[BlockStorageQuotaBase, QuotaBase](
        base=BlockStorageQuotaBase, base_public=QuotaBase
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
