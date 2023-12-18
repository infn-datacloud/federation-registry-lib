"""BlockStorageService specific fixtures."""
from typing import Any

from pytest_cases import fixture, parametrize

from app.provider.schemas_extended import (
    BlockStorageServiceCreateExtended,
)
from app.service.models import BlockStorageService
from app.service.schemas import (
    BlockStorageServiceBase,
    BlockStorageServiceRead,
    BlockStorageServiceReadPublic,
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


@fixture
def block_storage_service_create_validator() -> (
    CreateSchemaValidation[
        BlockStorageServiceBase,
        ServiceBase,
        BlockStorageServiceCreateExtended,
    ]
):
    """Instance to validate block_storage_service create schemas."""
    return CreateSchemaValidation[
        BlockStorageServiceBase,
        ServiceBase,
        BlockStorageServiceCreateExtended,
    ](
        base=BlockStorageServiceBase,
        base_public=ServiceBase,
        create=BlockStorageServiceCreateExtended,
    )


@fixture
def block_storage_service_read_validator() -> (
    ReadSchemaValidation[
        BlockStorageServiceBase,
        ServiceBase,
        BlockStorageServiceRead,
        BlockStorageServiceReadPublic,
        BlockStorageServiceReadExtended,
        BlockStorageServiceReadExtendedPublic,
        BlockStorageService,
    ]
):
    """Instance to validate block_storage_service read schemas."""
    return ReadSchemaValidation[
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


@fixture
def block_storage_service_patch_validator() -> (
    PatchSchemaValidation[BlockStorageServiceBase, ServiceBase]
):
    """Instance to validate block_storage_service patch schemas."""
    return PatchSchemaValidation[BlockStorageServiceBase, ServiceBase](
        base=BlockStorageServiceBase, base_public=ServiceBase
    )


@fixture
@parametrize(
    cls=[
        BlockStorageServiceRead,
        BlockStorageServiceReadExtended,
        BlockStorageServiceReadPublic,
        BlockStorageServiceReadExtendedPublic,
    ],
)
def block_storage_service_read_class(cls) -> Any:
    """BlockStorageService Read schema."""
    return cls
