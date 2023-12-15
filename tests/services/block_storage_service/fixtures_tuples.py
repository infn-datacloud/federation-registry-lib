"""BlockStorageService specific fixtures."""
from typing import Any, Dict, Tuple, Type, Union

from pytest_cases import fixture

from app.provider.schemas_extended import (
    BlockStorageServiceCreateExtended,
)
from app.service.models import BlockStorageService
from app.service.schemas import (
    BlockStorageServiceBase,
    BlockStorageServiceRead,
    BlockStorageServiceReadPublic,
    BlockStorageServiceUpdate,
    ServiceBase,
)
from app.service.schemas_extended import (
    BlockStorageServiceReadExtended,
    BlockStorageServiceReadExtendedPublic,
)
from tests.common.schema_validators import (
    BaseSchemaValidation,
    CreateSchemaValidation,
    ReadSchemaValidation,
)


@fixture
def block_storage_service_valid_create_schema_tuple(
    block_storage_service_create_validator, block_storage_service_create_valid_data
) -> Tuple[
    Type[BlockStorageServiceCreateExtended],
    CreateSchemaValidation[
        BlockStorageServiceBase,
        ServiceBase,
        BlockStorageServiceCreateExtended,
    ],
    Dict[str, Any],
]:
    """Fixture with the create class, validator and data to validate."""
    return (
        BlockStorageServiceCreateExtended,
        block_storage_service_create_validator,
        block_storage_service_create_valid_data,
    )


@fixture
def block_storage_service_invalid_create_schema_tuple(
    block_storage_service_create_invalid_data,
) -> Tuple[Type[BlockStorageServiceCreateExtended], Dict[str, Any]]:
    """Fixture with the create class and the invalid data to validate."""
    return BlockStorageServiceCreateExtended, block_storage_service_create_invalid_data


@fixture
def block_storage_service_valid_patch_schema_tuple(
    block_storage_service_patch_validator, block_storage_service_patch_valid_data
) -> Tuple[
    Type[BlockStorageServiceUpdate],
    BaseSchemaValidation[BlockStorageServiceBase, ServiceBase],
    Dict[str, Any],
]:
    """Fixture with the update class, validator and data to validate."""
    return (
        BlockStorageServiceUpdate,
        block_storage_service_patch_validator,
        block_storage_service_patch_valid_data,
    )


@fixture
def block_storage_service_invalid_patch_schema_tuple(
    block_storage_service_patch_invalid_data,
) -> Tuple[Type[BlockStorageServiceUpdate], Dict[str, Any]]:
    """Fixture with the update class and the invalid data to validate."""
    return BlockStorageServiceUpdate, block_storage_service_patch_invalid_data


@fixture
def block_storage_service_valid_read_schema_tuple(
    block_storage_service_read_class,
    block_storage_service_read_validator,
    db_block_storage_service,
) -> Tuple[
    Union[
        BlockStorageServiceRead,
        BlockStorageServiceReadPublic,
        BlockStorageServiceReadExtended,
        BlockStorageServiceReadExtendedPublic,
    ],
    ReadSchemaValidation[
        BlockStorageServiceBase,
        ServiceBase,
        BlockStorageServiceRead,
        BlockStorageServiceReadPublic,
        BlockStorageServiceReadExtended,
        BlockStorageServiceReadExtendedPublic,
        BlockStorageService,
    ],
    BlockStorageService,
]:
    """Fixture with the read class, validator and the db item to read."""
    return (
        block_storage_service_read_class,
        block_storage_service_read_validator,
        db_block_storage_service,
    )
