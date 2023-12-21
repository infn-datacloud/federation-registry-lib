"""NetworkService specific cases."""
from typing import Any, Dict, Tuple, Type, Union

from pytest_cases import case, parametrize

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
from tests.common.utils import detect_public_extended_details


@case(tags="create_valid")
def case_network_service_create_valid_schema_actors(
    network_service_create_valid_data: Dict[str, Any],
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


@case(tags="create_invalid")
def case_network_service_create_invalid_schema_actors(
    network_service_create_invalid_data: Dict[str, Any],
) -> Tuple[Type[NetworkServiceCreateExtended], Dict[str, Any]]:
    """Fixture with the create class and the invalid data to validate."""
    return NetworkServiceCreateExtended, network_service_create_invalid_data


@case(tags="patch_valid")
def case_network_service_patch_valid_schema_actors(
    network_service_patch_valid_data: Dict[str, Any],
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


@case(tags="patch_invalid")
def case_network_service_patch_invalid_schema_actors(
    network_service_patch_invalid_data: Dict[str, Any],
) -> Tuple[Type[NetworkServiceUpdate], Dict[str, Any]]:
    """Fixture with the update class and the invalid data to validate."""
    return NetworkServiceUpdate, network_service_patch_invalid_data


@case(tags="read")
@parametrize(
    cls=[
        NetworkServiceRead,
        NetworkServiceReadExtended,
        NetworkServiceReadPublic,
        NetworkServiceReadExtendedPublic,
    ],
)
def case_network_service_valid_read_schema_tuple(
    cls: Union[
        NetworkServiceRead,
        NetworkServiceReadPublic,
        NetworkServiceReadExtended,
        NetworkServiceReadExtendedPublic,
    ],
    db_network_service: NetworkService,
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
    is_public, is_extended = detect_public_extended_details(cls)
    return cls, validator, db_network_service, is_public, is_extended
