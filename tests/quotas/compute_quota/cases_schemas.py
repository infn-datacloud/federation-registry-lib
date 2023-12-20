"""ComputeQuota specific cases."""
from typing import Any, Dict, Tuple, Type, Union

from pytest_cases import case, parametrize

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


@case(tags="create_valid")
def case_compute_quota_create_valid_schema_actors(
    compute_quota_create_valid_data: Dict[str, Any],
) -> Tuple[
    Type[ComputeQuotaCreateExtended],
    CreateSchemaValidation[ComputeQuotaBase, QuotaBase, ComputeQuotaCreateExtended],
    Dict[str, Any],
]:
    """Fixture with the create class, validator and data to validate."""
    validator = CreateSchemaValidation[
        ComputeQuotaBase,
        QuotaBase,
        ComputeQuotaCreateExtended,
    ](
        base=ComputeQuotaBase,
        base_public=QuotaBase,
        create=ComputeQuotaCreateExtended,
    )
    return ComputeQuotaCreateExtended, validator, compute_quota_create_valid_data


@case(tags="create_invalid")
def case_compute_quota_create_invalid_schema_actors(
    compute_quota_create_invalid_data: Dict[str, Any],
) -> Tuple[Type[ComputeQuotaCreateExtended], Dict[str, Any]]:
    """Fixture with the create class and the invalid data to validate."""
    return ComputeQuotaCreateExtended, compute_quota_create_invalid_data


@case(tags="patch_valid")
def case_compute_quota_patch_valid_schema_actors(
    compute_quota_patch_valid_data: Dict[str, Any],
) -> Tuple[
    Type[ComputeQuotaUpdate],
    PatchSchemaValidation[ComputeQuotaBase, QuotaBase],
    Dict[str, Any],
]:
    """Fixture with the update class, validator and data to validate."""
    validator = PatchSchemaValidation[ComputeQuotaBase, QuotaBase](
        base=ComputeQuotaBase, base_public=QuotaBase
    )
    return ComputeQuotaUpdate, validator, compute_quota_patch_valid_data


@case(tags="patch_invalid")
def case_compute_quota_patch_invalid_schema_actors(
    compute_quota_patch_invalid_data: Dict[str, Any],
) -> Tuple[Type[ComputeQuotaUpdate], Dict[str, Any]]:
    """Fixture with the update class and the invalid data to validate."""
    return ComputeQuotaUpdate, compute_quota_patch_invalid_data


@case(tags="read")
@parametrize(
    cls=[
        ComputeQuotaRead,
        ComputeQuotaReadExtended,
        ComputeQuotaReadPublic,
        ComputeQuotaReadExtendedPublic,
    ],
)
def case_compute_quota_valid_read_schema_tuple(
    cls: Union[
        ComputeQuotaRead,
        ComputeQuotaReadPublic,
        ComputeQuotaReadExtended,
        ComputeQuotaReadExtendedPublic,
    ],
    db_compute_quota: ComputeQuota,
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
    validator = ReadSchemaValidation[
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
    cls_name = cls.__name__
    is_public = False
    is_extended = False
    if "Public" in cls_name:
        is_public = True
    if "Extended" in cls_name:
        is_extended = True
    return cls, validator, db_compute_quota, is_public, is_extended
