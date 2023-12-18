"""NetworkQuota specific fixtures."""
from typing import Any, Dict, Tuple, Type, Union

from pytest_cases import fixture

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
from tests.common.schema_validators import (
    CreateSchemaValidation,
    PatchSchemaValidation,
    ReadSchemaValidation,
)


@fixture
def network_quota_valid_create_schema_tuple(
    network_quota_create_validator, network_quota_create_valid_data
) -> Tuple[
    Type[NetworkQuotaCreateExtended],
    CreateSchemaValidation[NetworkQuotaBase, QuotaBase, NetworkQuotaCreateExtended],
    Dict[str, Any],
]:
    """Fixture with the create class, validator and data to validate."""
    return (
        NetworkQuotaCreateExtended,
        network_quota_create_validator,
        network_quota_create_valid_data,
    )


@fixture
def network_quota_invalid_create_schema_tuple(
    network_quota_create_invalid_data,
) -> Tuple[Type[NetworkQuotaCreateExtended], Dict[str, Any]]:
    """Fixture with the create class and the invalid data to validate."""
    return NetworkQuotaCreateExtended, network_quota_create_invalid_data


@fixture
def network_quota_valid_patch_schema_tuple(
    network_quota_patch_validator, network_quota_patch_valid_data
) -> Tuple[
    Type[NetworkQuotaUpdate],
    PatchSchemaValidation[NetworkQuotaBase, QuotaBase],
    Dict[str, Any],
]:
    """Fixture with the update class, validator and data to validate."""
    return (
        NetworkQuotaUpdate,
        network_quota_patch_validator,
        network_quota_patch_valid_data,
    )


@fixture
def network_quota_invalid_patch_schema_tuple(
    network_quota_patch_invalid_data,
) -> Tuple[Type[NetworkQuotaUpdate], Dict[str, Any]]:
    """Fixture with the update class and the invalid data to validate."""
    return NetworkQuotaUpdate, network_quota_patch_invalid_data


@fixture
def network_quota_valid_read_schema_tuple(
    network_quota_read_class,
    network_quota_read_validator,
    db_network_quota,
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
    return (
        network_quota_read_class,
        network_quota_read_validator,
        db_network_quota,
    )
