"""BlockStorageService specific cases."""
from typing import Any, Dict, Tuple, Type, Union

from pytest_cases import case, parametrize

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
from tests.common.schemas.validators import (
    CreateSchemaValidation,
    PatchSchemaValidation,
    ReadSchemaValidation,
)
from tests.common.utils import detect_public_extended_details


@case(tags="create_valid")
def case_block_storage_service_create_valid_schema_actors(
    block_storage_service_create_valid_data: Dict[str, Any],
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
    validator = CreateSchemaValidation[
        BlockStorageServiceBase,
        ServiceBase,
        BlockStorageServiceCreateExtended,
    ](
        base=BlockStorageServiceBase,
        base_public=ServiceBase,
        create=BlockStorageServiceCreateExtended,
    )
    return (
        BlockStorageServiceCreateExtended,
        validator,
        block_storage_service_create_valid_data,
    )


@case(tags="create_invalid")
def case_block_storage_service_create_invalid_schema_actors(
    block_storage_service_create_invalid_data: Dict[str, Any],
) -> Tuple[Type[BlockStorageServiceCreateExtended], Dict[str, Any]]:
    """Fixture with the create class and the invalid data to validate."""
    return BlockStorageServiceCreateExtended, block_storage_service_create_invalid_data


@case(tags="patch_valid")
def case_block_storage_service_patch_valid_schema_actors(
    block_storage_service_patch_valid_data: Dict[str, Any],
) -> Tuple[
    Type[BlockStorageServiceUpdate],
    PatchSchemaValidation[BlockStorageServiceBase, ServiceBase],
    Dict[str, Any],
]:
    """Fixture with the update class, validator and data to validate."""
    validator = PatchSchemaValidation[BlockStorageServiceBase, ServiceBase](
        base=BlockStorageServiceBase, base_public=ServiceBase
    )
    return (
        BlockStorageServiceUpdate,
        validator,
        block_storage_service_patch_valid_data,
    )


@case(tags="patch_invalid")
def case_block_storage_service_patch_invalid_schema_actors(
    block_storage_service_patch_invalid_data: Dict[str, Any],
) -> Tuple[Type[BlockStorageServiceUpdate], Dict[str, Any]]:
    """Fixture with the update class and the invalid data to validate."""
    return BlockStorageServiceUpdate, block_storage_service_patch_invalid_data


@case(tags="read")
@parametrize(
    cls=[
        BlockStorageServiceRead,
        BlockStorageServiceReadExtended,
        BlockStorageServiceReadPublic,
        BlockStorageServiceReadExtendedPublic,
    ],
)
def case_block_storage_service_valid_read_schema_tuple(
    cls: Union[
        BlockStorageServiceRead,
        BlockStorageServiceReadPublic,
        BlockStorageServiceReadExtended,
        BlockStorageServiceReadExtendedPublic,
    ],
    db_block_storage_service: BlockStorageService,
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
    validator = ReadSchemaValidation[
        BlockStorageServiceBase,
        ServiceBase,
        BlockStorageServiceRead,
        BlockStorageServiceReadPublic,
        BlockStorageServiceReadExtended,
        BlockStorageServiceReadExtendedPublic,
        BlockStorageService,
    ](
        base=BlockStorageServiceBase,
        base_public=ServiceBase,
        read=BlockStorageServiceRead,
        read_extended=BlockStorageServiceReadExtended,
    )
    is_public, is_extended = detect_public_extended_details(cls)
    return cls, validator, db_block_storage_service, is_public, is_extended
