"""NetworkQuota specific cases."""
from typing import Any, Dict, Tuple, Type, Union

from pytest_cases import case, parametrize

from app.provider.schemas_extended import (
    NetworkQuotaCreateExtended,
)
from app.quota.models import NetworkQuota
from app.quota.schemas import (
    NetworkQuotaBase,
    NetworkQuotaRead,
    NetworkQuotaReadPublic,
    NetworkQuotaUpdate,
    QuotaBase,
)
from app.quota.schemas_extended import (
    NetworkQuotaReadExtended,
    NetworkQuotaReadExtendedPublic,
)
from tests.common.schemas.validators import (
    CreateSchemaValidation,
    PatchSchemaValidation,
    ReadSchemaValidation,
)
from tests.common.utils import detect_public_extended_details


@case(tags="create_valid")
def case_network_quota_create_valid_schema_actors(
    network_quota_create_valid_data: Dict[str, Any],
) -> Tuple[
    Type[NetworkQuotaCreateExtended],
    CreateSchemaValidation[NetworkQuotaBase, QuotaBase, NetworkQuotaCreateExtended],
    Dict[str, Any],
]:
    """Fixture with the create class, validator and data to validate."""
    validator = CreateSchemaValidation[
        NetworkQuotaBase,
        QuotaBase,
        NetworkQuotaCreateExtended,
    ](
        base=NetworkQuotaBase,
        base_public=QuotaBase,
        create=NetworkQuotaCreateExtended,
    )
    return (NetworkQuotaCreateExtended, validator, network_quota_create_valid_data)


@case(tags="create_invalid")
def case_network_quota_create_invalid_schema_actors(
    network_quota_create_invalid_data: Dict[str, Any],
) -> Tuple[Type[NetworkQuotaCreateExtended], Dict[str, Any]]:
    """Fixture with the create class and the invalid data to validate."""
    return NetworkQuotaCreateExtended, network_quota_create_invalid_data


@case(tags="patch_valid")
def case_network_quota_patch_valid_schema_actors(
    network_quota_patch_valid_data: Dict[str, Any],
) -> Tuple[
    Type[NetworkQuotaUpdate],
    PatchSchemaValidation[NetworkQuotaBase, QuotaBase],
    Dict[str, Any],
]:
    """Fixture with the update class, validator and data to validate."""
    validator = PatchSchemaValidation[NetworkQuotaBase, QuotaBase](
        base=NetworkQuotaBase, base_public=QuotaBase
    )
    return (NetworkQuotaUpdate, validator, network_quota_patch_valid_data)


@case(tags="patch_invalid")
def case_network_quota_patch_invalid_schema_actors(
    network_quota_patch_invalid_data: Dict[str, Any],
) -> Tuple[Type[NetworkQuotaUpdate], Dict[str, Any]]:
    """Fixture with the update class and the invalid data to validate."""
    return NetworkQuotaUpdate, network_quota_patch_invalid_data


@case(tags="read")
@parametrize(
    cls=[
        NetworkQuotaRead,
        NetworkQuotaReadExtended,
        NetworkQuotaReadPublic,
        NetworkQuotaReadExtendedPublic,
    ],
)
def case_network_quota_valid_read_schema_tuple(
    cls: Union[
        NetworkQuotaRead,
        NetworkQuotaReadPublic,
        NetworkQuotaReadExtended,
        NetworkQuotaReadExtendedPublic,
    ],
    db_network_quota: NetworkQuota,
) -> Tuple[
    Union[
        NetworkQuotaRead,
        NetworkQuotaReadPublic,
        NetworkQuotaReadExtended,
        NetworkQuotaReadExtendedPublic,
    ],
    ReadSchemaValidation[
        NetworkQuotaBase,
        QuotaBase,
        NetworkQuotaRead,
        NetworkQuotaReadPublic,
        NetworkQuotaReadExtended,
        NetworkQuotaReadExtendedPublic,
        NetworkQuota,
    ],
    NetworkQuota,
]:
    """Fixture with the read class, validator and the db item to read."""
    validator = ReadSchemaValidation[
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
    is_public, is_extended = detect_public_extended_details(cls)
    return cls, validator, db_network_quota, is_public, is_extended
