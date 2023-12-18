"""NetworkService specific fixtures."""
from typing import Any, Dict, Tuple, Type, Union

from pytest_cases import fixture

from app.provider.schemas_extended import (
    NetworkServiceCreateExtended,
)
from app.service.models import NetworkService
from app.service.schemas import (
    NetworkServiceBase,
    NetworkServiceRead,
    NetworkServiceReadPublic,
    NetworkServiceUpdate,
    ServiceBase,
)
from app.service.schemas_extended import (
    NetworkServiceReadExtended,
    NetworkServiceReadExtendedPublic,
)
from tests.common.schema_validators import (
    CreateSchemaValidation,
    PatchSchemaValidation,
    ReadSchemaValidation,
)


@fixture
def network_service_valid_create_schema_tuple(
    network_service_create_validator, network_service_create_valid_data
) -> Tuple[
    Type[NetworkServiceCreateExtended],
    CreateSchemaValidation[
        NetworkServiceBase,
        ServiceBase,
        NetworkServiceCreateExtended,
    ],
    Dict[str, Any],
]:
    """Fixture with the create class, validator and data to validate."""
    return (
        NetworkServiceCreateExtended,
        network_service_create_validator,
        network_service_create_valid_data,
    )


@fixture
def network_service_invalid_create_schema_tuple(
    network_service_create_invalid_data,
) -> Tuple[Type[NetworkServiceCreateExtended], Dict[str, Any]]:
    """Fixture with the create class and the invalid data to validate."""
    return NetworkServiceCreateExtended, network_service_create_invalid_data


@fixture
def network_service_valid_patch_schema_tuple(
    network_service_patch_validator, network_service_patch_valid_data
) -> Tuple[
    Type[NetworkServiceUpdate],
    PatchSchemaValidation[NetworkServiceBase, ServiceBase],
    Dict[str, Any],
]:
    """Fixture with the update class, validator and data to validate."""
    return (
        NetworkServiceUpdate,
        network_service_patch_validator,
        network_service_patch_valid_data,
    )


@fixture
def network_service_invalid_patch_schema_tuple(
    network_service_patch_invalid_data,
) -> Tuple[Type[NetworkServiceUpdate], Dict[str, Any]]:
    """Fixture with the update class and the invalid data to validate."""
    return NetworkServiceUpdate, network_service_patch_invalid_data


@fixture
def network_service_valid_read_schema_tuple(
    network_service_read_class,
    network_service_read_validator,
    db_network_service,
) -> Tuple[
    Union[
        NetworkServiceRead,
        NetworkServiceReadPublic,
        NetworkServiceReadExtended,
        NetworkServiceReadExtendedPublic,
    ],
    ReadSchemaValidation[
        NetworkServiceBase,
        ServiceBase,
        NetworkServiceRead,
        NetworkServiceReadPublic,
        NetworkServiceReadExtended,
        NetworkServiceReadExtendedPublic,
        NetworkService,
    ],
    NetworkService,
]:
    """Fixture with the read class, validator and the db item to read."""
    return (
        network_service_read_class,
        network_service_read_validator,
        db_network_service,
    )
