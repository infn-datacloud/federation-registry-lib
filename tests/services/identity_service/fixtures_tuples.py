"""IdentityService specific fixtures."""
from typing import Any, Dict, Tuple, Type, Union

from pytest_cases import fixture

from app.provider.schemas_extended import (
    IdentityServiceCreate,
)
from app.service.models import IdentityService
from app.service.schemas import (
    IdentityServiceBase,
    IdentityServiceRead,
    IdentityServiceReadPublic,
    IdentityServiceUpdate,
    ServiceBase,
)
from app.service.schemas_extended import (
    IdentityServiceReadExtended,
    IdentityServiceReadExtendedPublic,
)
from tests.common.schema_validators import (
    BaseSchemaValidation,
    CreateSchemaValidation,
    ReadSchemaValidation,
)


@fixture
def identity_service_valid_create_schema_tuple(
    identity_service_create_validator, identity_service_create_valid_data
) -> Tuple[
    Type[IdentityServiceCreate],
    CreateSchemaValidation[
        IdentityServiceBase,
        ServiceBase,
        IdentityServiceCreate,
    ],
    Dict[str, Any],
]:
    """Fixture with the create class, validator and data to validate."""
    return (
        IdentityServiceCreate,
        identity_service_create_validator,
        identity_service_create_valid_data,
    )


@fixture
def identity_service_invalid_create_schema_tuple(
    identity_service_create_invalid_data,
) -> Tuple[Type[IdentityServiceCreate], Dict[str, Any]]:
    """Fixture with the create class and the invalid data to validate."""
    return IdentityServiceCreate, identity_service_create_invalid_data


@fixture
def identity_service_valid_patch_schema_tuple(
    identity_service_patch_validator, identity_service_patch_valid_data
) -> Tuple[
    Type[IdentityServiceUpdate],
    BaseSchemaValidation[IdentityServiceBase, ServiceBase],
    Dict[str, Any],
]:
    """Fixture with the update class, validator and data to validate."""
    return (
        IdentityServiceUpdate,
        identity_service_patch_validator,
        identity_service_patch_valid_data,
    )


@fixture
def identity_service_invalid_patch_schema_tuple(
    identity_service_patch_invalid_data,
) -> Tuple[Type[IdentityServiceUpdate], Dict[str, Any]]:
    """Fixture with the update class and the invalid data to validate."""
    return IdentityServiceUpdate, identity_service_patch_invalid_data


@fixture
def identity_service_valid_read_schema_tuple(
    identity_service_read_class,
    identity_service_read_validator,
    db_identity_service,
) -> Tuple[
    Union[
        IdentityServiceRead,
        IdentityServiceReadPublic,
        IdentityServiceReadExtended,
        IdentityServiceReadExtendedPublic,
    ],
    ReadSchemaValidation[
        IdentityServiceBase,
        ServiceBase,
        IdentityServiceRead,
        IdentityServiceReadPublic,
        IdentityServiceReadExtended,
        IdentityServiceReadExtendedPublic,
        IdentityService,
    ],
    IdentityService,
]:
    """Fixture with the read class, validator and the db item to read."""
    return (
        identity_service_read_class,
        identity_service_read_validator,
        db_identity_service,
    )
