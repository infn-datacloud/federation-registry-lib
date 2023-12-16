"""NetworkService specific fixtures."""
from typing import Any

from pytest_cases import fixture, parametrize

from app.provider.schemas_extended import (
    NetworkServiceCreateExtended,
)
from app.service.models import NetworkService
from app.service.schemas import (
    NetworkServiceBase,
    NetworkServiceRead,
    NetworkServiceReadPublic,
    ServiceBase,
)
from app.service.schemas_extended import (
    NetworkServiceReadExtended,
    NetworkServiceReadExtendedPublic,
)
from tests.common.schema_validators import (
    BaseSchemaValidation,
    CreateSchemaValidation,
    ReadSchemaValidation,
)


@fixture
def network_service_create_validator() -> (
    CreateSchemaValidation[
        NetworkServiceBase,
        ServiceBase,
        NetworkServiceCreateExtended,
    ]
):
    """Instance to validate network_service create schemas."""
    return CreateSchemaValidation[
        NetworkServiceBase,
        ServiceBase,
        NetworkServiceCreateExtended,
    ](
        base=NetworkServiceBase,
        base_public=ServiceBase,
        create=NetworkServiceCreateExtended,
    )


@fixture
def network_service_read_validator() -> (
    ReadSchemaValidation[
        NetworkServiceBase,
        ServiceBase,
        NetworkServiceRead,
        NetworkServiceReadPublic,
        NetworkServiceReadExtended,
        NetworkServiceReadExtendedPublic,
        NetworkService,
    ]
):
    """Instance to validate network_service read schemas."""
    return ReadSchemaValidation[
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


@fixture
def network_service_patch_validator() -> (
    BaseSchemaValidation[NetworkServiceBase, ServiceBase]
):
    """Instance to validate network_service patch schemas."""
    return BaseSchemaValidation[NetworkServiceBase, ServiceBase](
        base=NetworkServiceBase, base_public=ServiceBase
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
