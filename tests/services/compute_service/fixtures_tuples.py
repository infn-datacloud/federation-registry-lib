"""ComputeService specific fixtures."""
from typing import Any, Dict, Tuple, Type, Union

from pytest_cases import fixture

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
from tests.common.schema_validators import (
    BaseSchemaValidation,
    CreateSchemaValidation,
    ReadSchemaValidation,
)


@fixture
def compute_service_valid_create_schema_tuple(
    compute_service_create_validator, compute_service_create_valid_data
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
    return (
        ComputeServiceCreateExtended,
        compute_service_create_validator,
        compute_service_create_valid_data,
    )


@fixture
def compute_service_invalid_create_schema_tuple(
    compute_service_create_invalid_data,
) -> Tuple[Type[ComputeServiceCreateExtended], Dict[str, Any]]:
    """Fixture with the create class and the invalid data to validate."""
    return ComputeServiceCreateExtended, compute_service_create_invalid_data


@fixture
def compute_service_valid_patch_schema_tuple(
    compute_service_patch_validator, compute_service_patch_valid_data
) -> Tuple[
    Type[ComputeServiceUpdate],
    BaseSchemaValidation[ComputeServiceBase, ServiceBase],
    Dict[str, Any],
]:
    """Fixture with the update class, validator and data to validate."""
    return (
        ComputeServiceUpdate,
        compute_service_patch_validator,
        compute_service_patch_valid_data,
    )


@fixture
def compute_service_invalid_patch_schema_tuple(
    compute_service_patch_invalid_data,
) -> Tuple[Type[ComputeServiceUpdate], Dict[str, Any]]:
    """Fixture with the update class and the invalid data to validate."""
    return ComputeServiceUpdate, compute_service_patch_invalid_data


@fixture
def compute_service_valid_read_schema_tuple(
    compute_service_read_class,
    compute_service_read_validator,
    db_compute_service,
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
    return (
        compute_service_read_class,
        compute_service_read_validator,
        db_compute_service,
    )
