"""ComputeService specific cases."""
from typing import Any, Dict, Tuple, Type, Union

from pytest_cases import case, parametrize

from app.provider.schemas_extended import (
    ComputeServiceCreateExtended,
)
from app.service.models import ComputeService
from app.service.schemas import (
    ComputeServiceBase,
    ComputeServiceRead,
    ComputeServiceReadPublic,
    ComputeServiceUpdate,
    ServiceBase,
)
from app.service.schemas_extended import (
    ComputeServiceReadExtended,
    ComputeServiceReadExtendedPublic,
)
from tests.common.schemas.validators import (
    CreateSchemaValidation,
    PatchSchemaValidation,
    ReadSchemaValidation,
)
from tests.common.utils import detect_public_extended_details


@case(tags="create_valid")
def case_compute_service_create_valid_schema_actors(
    compute_service_create_valid_data: Dict[str, Any],
) -> Tuple[
    Type[ComputeServiceCreateExtended],
    CreateSchemaValidation[
        ComputeServiceBase,
        ServiceBase,
        ComputeServiceCreateExtended,
    ],
    Dict[str, Any],
]:
    """Fixture with the create class, validator and data to validate."""
    validator = CreateSchemaValidation[
        ComputeServiceBase,
        ServiceBase,
        ComputeServiceCreateExtended,
    ](
        base=ComputeServiceBase,
        base_public=ServiceBase,
        create=ComputeServiceCreateExtended,
    )
    return (ComputeServiceCreateExtended, validator, compute_service_create_valid_data)


@case(tags="create_invalid")
def case_compute_service_create_invalid_schema_actors(
    compute_service_create_invalid_data: Dict[str, Any],
) -> Tuple[Type[ComputeServiceCreateExtended], Dict[str, Any]]:
    """Fixture with the create class and the invalid data to validate."""
    return ComputeServiceCreateExtended, compute_service_create_invalid_data


@case(tags="patch_valid")
def case_compute_service_patch_valid_schema_actors(
    compute_service_patch_valid_data: Dict[str, Any],
) -> Tuple[
    Type[ComputeServiceUpdate],
    PatchSchemaValidation[ComputeServiceBase, ServiceBase],
    Dict[str, Any],
]:
    """Fixture with the update class, validator and data to validate."""
    validator = PatchSchemaValidation[ComputeServiceBase, ServiceBase](
        base=ComputeServiceBase, base_public=ServiceBase
    )
    return ComputeServiceUpdate, validator, compute_service_patch_valid_data


@case(tags="patch_invalid")
def case_compute_service_patch_invalid_schema_actors(
    compute_service_patch_invalid_data: Dict[str, Any],
) -> Tuple[Type[ComputeServiceUpdate], Dict[str, Any]]:
    """Fixture with the update class and the invalid data to validate."""
    return ComputeServiceUpdate, compute_service_patch_invalid_data


@case(tags="read")
@parametrize(
    cls=[
        ComputeServiceRead,
        ComputeServiceReadExtended,
        ComputeServiceReadPublic,
        ComputeServiceReadExtendedPublic,
    ],
)
def case_compute_service_valid_read_schema_tuple(
    cls: Union[
        ComputeServiceRead,
        ComputeServiceReadPublic,
        ComputeServiceReadExtended,
        ComputeServiceReadExtendedPublic,
    ],
    db_compute_service: ComputeService,
) -> Tuple[
    Union[
        ComputeServiceRead,
        ComputeServiceReadPublic,
        ComputeServiceReadExtended,
        ComputeServiceReadExtendedPublic,
    ],
    ReadSchemaValidation[
        ComputeServiceBase,
        ServiceBase,
        ComputeServiceRead,
        ComputeServiceReadPublic,
        ComputeServiceReadExtended,
        ComputeServiceReadExtendedPublic,
        ComputeService,
    ],
    ComputeService,
]:
    """Fixture with the read class, validator and the db item to read."""
    validator = ReadSchemaValidation[
        ComputeServiceBase,
        ServiceBase,
        ComputeServiceRead,
        ComputeServiceReadPublic,
        ComputeServiceReadExtended,
        ComputeServiceReadExtendedPublic,
        ComputeService,
    ](
        base=ComputeServiceBase,
        base_public=ServiceBase,
        read=ComputeServiceRead,
        read_extended=ComputeServiceReadExtended,
    )
    is_public, is_extended = detect_public_extended_details(cls)
    return cls, validator, db_compute_service, is_public, is_extended
