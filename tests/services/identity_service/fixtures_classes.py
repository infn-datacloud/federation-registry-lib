"""IdentityService specific fixtures."""
from typing import Any

from pytest_cases import fixture, parametrize

from app.provider.schemas_extended import (
    IdentityServiceCreate,
)
from app.service.models import IdentityService
from app.service.schemas import (
    IdentityServiceBase,
    IdentityServiceRead,
    IdentityServiceReadPublic,
    ServiceBase,
)
from app.service.schemas_extended import (
    IdentityServiceReadExtended,
    IdentityServiceReadExtendedPublic,
)
from tests.common.schema_validators import (
    BaseSchemaValidation,
    CreateSchemaValidation,
    ReadSchemaValidation,
)


@fixture
def identity_service_create_validator() -> (
    CreateSchemaValidation[
        IdentityServiceBase,
        ServiceBase,
        IdentityServiceCreate,
    ]
):
    """Instance to validate identity_service create schemas."""
    return CreateSchemaValidation[
        IdentityServiceBase,
        ServiceBase,
        IdentityServiceCreate,
    ](
        base=IdentityServiceBase,
        base_public=ServiceBase,
        create=IdentityServiceCreate,
    )


@fixture
def identity_service_read_validator() -> (
    ReadSchemaValidation[
        IdentityServiceBase,
        ServiceBase,
        IdentityServiceRead,
        IdentityServiceReadPublic,
        IdentityServiceReadExtended,
        IdentityServiceReadExtendedPublic,
        IdentityService,
    ]
):
    """Instance to validate identity_service read schemas."""
    return ReadSchemaValidation[
        IdentityServiceBase,
        ServiceBase,
        IdentityServiceRead,
        IdentityServiceReadPublic,
        IdentityServiceReadExtended,
        IdentityServiceReadExtendedPublic,
        IdentityService,
    ](
        base=IdentityServiceBase,
        base_public=ServiceBase,
        read=IdentityServiceRead,
        read_extended=IdentityServiceReadExtended,
    )


@fixture
def identity_service_patch_validator() -> (
    BaseSchemaValidation[IdentityServiceBase, ServiceBase]
):
    """Instance to validate identity_service patch schemas."""
    return BaseSchemaValidation[IdentityServiceBase, ServiceBase](
        base=IdentityServiceBase, base_public=ServiceBase
    )


@fixture
@parametrize(
    "cls",
    {
        IdentityServiceRead,
        IdentityServiceReadExtended,
        IdentityServiceReadPublic,
        IdentityServiceReadExtendedPublic,
    },
)
def identity_service_read_class(cls) -> Any:
    """IdentityService Read schema."""
    return cls
