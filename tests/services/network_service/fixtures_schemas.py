"""NetworkService specific fixtures."""
from typing import Any, Dict, Tuple, Type, Union

from pytest_cases import fixture, parametrize

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
from tests.common.schemas.validators import (
    CreateSchemaValidation,
    PatchSchemaValidation,
    ReadSchemaValidation,
)


@fixture
@parametrize(
    cls=[
        NetworkServiceRead,
        NetworkServiceReadExtended,
        NetworkServiceReadPublic,
        NetworkServiceReadExtendedPublic,
    ],
)
def network_service_read_class(cls) -> Any:
    """NetworkService Read schema."""
    return cls


@fixture
def network_service_valid_create_schema_tuple(
    network_service_create_valid_data,
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
    validator = CreateSchemaValidation[
        NetworkServiceBase,
        ServiceBase,
        NetworkServiceCreateExtended,
    ](
        base=NetworkServiceBase,
        base_public=ServiceBase,
        create=NetworkServiceCreateExtended,
    )
    return NetworkServiceCreateExtended, validator, network_service_create_valid_data


@fixture
def network_service_invalid_create_schema_tuple(
    network_service_create_invalid_data,
) -> Tuple[Type[NetworkServiceCreateExtended], Dict[str, Any]]:
    """Fixture with the create class and the invalid data to validate."""
    return NetworkServiceCreateExtended, network_service_create_invalid_data


@fixture
def network_service_valid_patch_schema_tuple(
    network_service_patch_valid_data,
) -> Tuple[
    Type[NetworkServiceUpdate],
    PatchSchemaValidation[NetworkServiceBase, ServiceBase],
    Dict[str, Any],
]:
    """Fixture with the update class, validator and data to validate."""
    validator = PatchSchemaValidation[NetworkServiceBase, ServiceBase](
        base=NetworkServiceBase, base_public=ServiceBase
    )
    return NetworkServiceUpdate, validator, network_service_patch_valid_data


@fixture
def network_service_invalid_patch_schema_tuple(
    network_service_patch_invalid_data,
) -> Tuple[Type[NetworkServiceUpdate], Dict[str, Any]]:
    """Fixture with the update class and the invalid data to validate."""
    return NetworkServiceUpdate, network_service_patch_invalid_data


@fixture
def network_service_valid_read_schema_tuple(
    network_service_read_class, db_network_service
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
    validator = ReadSchemaValidation[
        NetworkServiceBase,
        ServiceBase,
        NetworkServiceRead,
        NetworkServiceReadPublic,
        NetworkServiceReadExtended,
        NetworkServiceReadExtendedPublic,
        NetworkService,
    ](
        base=NetworkServiceBase,
        base_public=ServiceBase,
        read=NetworkServiceRead,
        read_extended=NetworkServiceReadExtended,
    )
    return network_service_read_class, validator, db_network_service
