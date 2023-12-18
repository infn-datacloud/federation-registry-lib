"""ComputeQuota specific fixtures."""
from typing import Any

from pytest_cases import fixture, parametrize

from app.provider.schemas_extended import (
    ComputeQuotaCreateExtended,
)
from app.quota.models import ComputeQuota
from app.quota.schemas import (
    ComputeQuotaBase,
    ComputeQuotaRead,
    ComputeQuotaReadPublic,
    QuotaBase,
)
from app.quota.schemas_extended import (
    ComputeQuotaReadExtended,
    ComputeQuotaReadExtendedPublic,
)
from tests.common.schema_validators import (
    CreateSchemaValidation,
    PatchSchemaValidation,
    ReadSchemaValidation,
)


@fixture
def compute_quota_create_validator() -> (
    CreateSchemaValidation[
        ComputeQuotaBase,
        QuotaBase,
        ComputeQuotaCreateExtended,
    ]
):
    """Instance to validate compute_quota create schemas."""
    return CreateSchemaValidation[
        ComputeQuotaBase,
        QuotaBase,
        ComputeQuotaCreateExtended,
    ](
        base=ComputeQuotaBase,
        base_public=QuotaBase,
        create=ComputeQuotaCreateExtended,
    )


@fixture
def compute_quota_read_validator() -> (
    ReadSchemaValidation[
        ComputeQuotaBase,
        QuotaBase,
        ComputeQuotaRead,
        ComputeQuotaReadPublic,
        ComputeQuotaReadExtended,
        ComputeQuotaReadExtendedPublic,
        ComputeQuota,
    ]
):
    """Instance to validate compute_quota read schemas."""
    return ReadSchemaValidation[
        ComputeQuotaBase,
        QuotaBase,
        ComputeQuotaRead,
        ComputeQuotaReadPublic,
        ComputeQuotaReadExtended,
        ComputeQuotaReadExtendedPublic,
        ComputeQuota,
    ](
        base=ComputeQuotaBase,
        base_public=QuotaBase,
        read=ComputeQuotaRead,
        read_extended=ComputeQuotaReadExtended,
    )


@fixture
def compute_quota_patch_validator() -> (
    PatchSchemaValidation[ComputeQuotaBase, QuotaBase]
):
    """Instance to validate compute_quota patch schemas."""
    return PatchSchemaValidation[ComputeQuotaBase, QuotaBase](
        base=ComputeQuotaBase, base_public=QuotaBase
    )


@fixture
@parametrize(
    cls=[
        ComputeQuotaRead,
        ComputeQuotaReadExtended,
        ComputeQuotaReadPublic,
        ComputeQuotaReadExtendedPublic,
    ],
)
def compute_quota_read_class(cls) -> Any:
    """ComputeQuota Read schema."""
    return cls
