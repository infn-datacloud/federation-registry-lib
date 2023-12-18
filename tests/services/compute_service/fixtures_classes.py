"""ComputeService specific fixtures."""
from typing import Any

from pytest_cases import fixture, parametrize

from app.provider.schemas_extended import (
    ComputeServiceCreateExtended,
)
from app.service.models import ComputeService
from app.service.schemas import (
    ComputeServiceBase,
    ComputeServiceRead,
    ComputeServiceReadPublic,
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


@fixture
def compute_service_create_validator() -> (
    CreateSchemaValidation[
        ComputeServiceBase,
        ServiceBase,
        ComputeServiceCreateExtended,
    ]
):
    """Instance to validate compute_service create schemas."""
    return CreateSchemaValidation[
        ComputeServiceBase,
        ServiceBase,
        ComputeServiceCreateExtended,
    ](
        base=ComputeServiceBase,
        base_public=ServiceBase,
        create=ComputeServiceCreateExtended,
    )


@fixture
def compute_service_read_validator() -> (
    ReadSchemaValidation[
        ComputeServiceBase,
        ServiceBase,
        ComputeServiceRead,
        ComputeServiceReadPublic,
        ComputeServiceReadExtended,
        ComputeServiceReadExtendedPublic,
        ComputeService,
    ]
):
    """Instance to validate compute_service read schemas."""
    return ReadSchemaValidation[
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


@fixture
def compute_service_patch_validator() -> (
    PatchSchemaValidation[ComputeServiceBase, ServiceBase]
):
    """Instance to validate compute_service patch schemas."""
    return PatchSchemaValidation[ComputeServiceBase, ServiceBase](
        base=ComputeServiceBase, base_public=ServiceBase
    )


@fixture
@parametrize(
    cls=[
        ComputeServiceRead,
        ComputeServiceReadExtended,
        ComputeServiceReadPublic,
        ComputeServiceReadExtendedPublic,
    ],
)
def compute_service_read_class(cls) -> Any:
    """ComputeService Read schema."""
    return cls
