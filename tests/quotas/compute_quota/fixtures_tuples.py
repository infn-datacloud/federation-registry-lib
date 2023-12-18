"""ComputeQuota specific fixtures."""
from typing import Any, Dict, Tuple, Type, Union

from pytest_cases import fixture

from app.provider.schemas_extended import (
    ComputeQuotaCreateExtended,
)
from app.quota.models import ComputeQuota
from app.quota.schemas import (
    ComputeQuotaBase,
    ComputeQuotaRead,
    ComputeQuotaReadPublic,
    ComputeQuotaUpdate,
    QuotaBase,
)
from app.quota.schemas_extended import (
    ComputeQuotaReadExtended,
    ComputeQuotaReadExtendedPublic,
)
from tests.common.schemas.validators import (
    CreateSchemaValidation,
    PatchSchemaValidation,
    ReadSchemaValidation,
)


@fixture
def compute_quota_valid_create_schema_tuple(
    compute_quota_create_validator, compute_quota_create_valid_data
) -> Tuple[
    Type[ComputeQuotaCreateExtended],
    CreateSchemaValidation[ComputeQuotaBase, QuotaBase, ComputeQuotaCreateExtended],
    Dict[str, Any],
]:
    """Fixture with the create class, validator and data to validate."""
    return (
        ComputeQuotaCreateExtended,
        compute_quota_create_validator,
        compute_quota_create_valid_data,
    )


@fixture
def compute_quota_invalid_create_schema_tuple(
    compute_quota_create_invalid_data,
) -> Tuple[Type[ComputeQuotaCreateExtended], Dict[str, Any]]:
    """Fixture with the create class and the invalid data to validate."""
    return ComputeQuotaCreateExtended, compute_quota_create_invalid_data


@fixture
def compute_quota_valid_patch_schema_tuple(
    compute_quota_patch_validator, compute_quota_patch_valid_data
) -> Tuple[
    Type[ComputeQuotaUpdate],
    PatchSchemaValidation[ComputeQuotaBase, QuotaBase],
    Dict[str, Any],
]:
    """Fixture with the update class, validator and data to validate."""
    return (
        ComputeQuotaUpdate,
        compute_quota_patch_validator,
        compute_quota_patch_valid_data,
    )


@fixture
def compute_quota_invalid_patch_schema_tuple(
    compute_quota_patch_invalid_data,
) -> Tuple[Type[ComputeQuotaUpdate], Dict[str, Any]]:
    """Fixture with the update class and the invalid data to validate."""
    return ComputeQuotaUpdate, compute_quota_patch_invalid_data


@fixture
def compute_quota_valid_read_schema_tuple(
    compute_quota_read_class,
    compute_quota_read_validator,
    db_compute_quota,
) -> Tuple[
    Union[
        ComputeQuotaRead,
        ComputeQuotaReadPublic,
        ComputeQuotaReadExtended,
        ComputeQuotaReadExtendedPublic,
    ],
    ReadSchemaValidation[
        ComputeQuotaBase,
        QuotaBase,
        ComputeQuotaRead,
        ComputeQuotaReadPublic,
        ComputeQuotaReadExtended,
        ComputeQuotaReadExtendedPublic,
        ComputeQuota,
    ],
    ComputeQuota,
]:
    """Fixture with the read class, validator and the db item to read."""
    return (
        compute_quota_read_class,
        compute_quota_read_validator,
        db_compute_quota,
    )
