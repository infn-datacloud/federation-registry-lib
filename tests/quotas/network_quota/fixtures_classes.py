"""NetworkQuota specific fixtures."""
from typing import Any

from pytest_cases import fixture, parametrize

from app.provider.schemas_extended import (
    NetworkQuotaCreateExtended,
)
from app.quota.models import NetworkQuota
from app.quota.schemas import (
    NetworkQuotaBase,
    NetworkQuotaRead,
    NetworkQuotaReadPublic,
    QuotaBase,
)
from app.quota.schemas_extended import (
    NetworkQuotaReadExtended,
    NetworkQuotaReadExtendedPublic,
)
from tests.common.schema_validators import (
    BaseSchemaValidation,
    CreateSchemaValidation,
    ReadSchemaValidation,
)


@fixture
def network_quota_create_validator() -> (
    CreateSchemaValidation[
        NetworkQuotaBase,
        QuotaBase,
        NetworkQuotaCreateExtended,
    ]
):
    """Instance to validate network_quota create schemas."""
    return CreateSchemaValidation[
        NetworkQuotaBase,
        QuotaBase,
        NetworkQuotaCreateExtended,
    ](
        base=NetworkQuotaBase,
        base_public=QuotaBase,
        create=NetworkQuotaCreateExtended,
    )


@fixture
def network_quota_read_validator() -> (
    ReadSchemaValidation[
        NetworkQuotaBase,
        QuotaBase,
        NetworkQuotaRead,
        NetworkQuotaReadPublic,
        NetworkQuotaReadExtended,
        NetworkQuotaReadExtendedPublic,
        NetworkQuota,
    ]
):
    """Instance to validate network_quota read schemas."""
    return ReadSchemaValidation[
        NetworkQuotaBase,
        QuotaBase,
        NetworkQuotaRead,
        NetworkQuotaReadPublic,
        NetworkQuotaReadExtended,
        NetworkQuotaReadExtendedPublic,
        NetworkQuota,
    ](
        base=NetworkQuotaBase,
        base_public=QuotaBase,
        read=NetworkQuotaRead,
        read_extended=NetworkQuotaReadExtended,
    )


@fixture
def network_quota_patch_validator() -> (
    BaseSchemaValidation[NetworkQuotaBase, QuotaBase]
):
    """Instance to validate network_quota patch schemas."""
    return BaseSchemaValidation[NetworkQuotaBase, QuotaBase](
        base=NetworkQuotaBase, base_public=QuotaBase
    )


@fixture
@parametrize(
    "cls",
    {
        NetworkQuotaRead,
        NetworkQuotaReadExtended,
        NetworkQuotaReadPublic,
        NetworkQuotaReadExtendedPublic,
    },
)
def network_quota_read_class(cls) -> Any:
    """NetworkQuota Read schema."""
    return cls
