"""IdentityProvider specific fixtures."""
from typing import Any

from pytest_cases import fixture, parametrize

from app.identity_provider.models import IdentityProvider
from app.identity_provider.schemas import (
    IdentityProviderBase,
    IdentityProviderBasePublic,
    IdentityProviderRead,
    IdentityProviderReadPublic,
)
from app.identity_provider.schemas_extended import (
    IdentityProviderReadExtended,
    IdentityProviderReadExtendedPublic,
)
from app.provider.schemas_extended import (
    IdentityProviderCreateExtended,
)
from tests.common.schema_validators import (
    BaseSchemaValidation,
    CreateSchemaValidation,
    ReadSchemaValidation,
)


@fixture
def identity_provider_create_validator() -> (
    CreateSchemaValidation[
        IdentityProviderBase, IdentityProviderBasePublic, IdentityProviderCreateExtended
    ]
):
    """Instance to validate identity_provider create schemas."""
    return CreateSchemaValidation[
        IdentityProviderBase, IdentityProviderBasePublic, IdentityProviderCreateExtended
    ](
        base=IdentityProviderBase,
        base_public=IdentityProviderBasePublic,
        create=IdentityProviderCreateExtended,
    )


@fixture
def identity_provider_read_validator() -> (
    ReadSchemaValidation[
        IdentityProviderBase,
        IdentityProviderBasePublic,
        IdentityProviderRead,
        IdentityProviderReadPublic,
        IdentityProviderReadExtended,
        IdentityProviderReadExtendedPublic,
        IdentityProvider,
    ]
):
    """Instance to validate identity_provider read schemas."""
    return ReadSchemaValidation[
        IdentityProviderBase,
        IdentityProviderBasePublic,
        IdentityProviderRead,
        IdentityProviderReadPublic,
        IdentityProviderReadExtended,
        IdentityProviderReadExtendedPublic,
        IdentityProvider,
    ](
        base=IdentityProviderBase,
        base_public=IdentityProviderBasePublic,
        read=IdentityProviderRead,
        read_extended=IdentityProviderReadExtended,
    )


@fixture
def identity_provider_patch_validator() -> (
    BaseSchemaValidation[IdentityProviderBase, IdentityProviderBasePublic]
):
    """Instance to validate identity_provider patch schemas."""
    return BaseSchemaValidation[IdentityProviderBase, IdentityProviderBasePublic](
        base=IdentityProviderBase, base_public=IdentityProviderBasePublic
    )


@fixture
@parametrize(
    cls=[
        IdentityProviderRead,
        IdentityProviderReadExtended,
        IdentityProviderReadPublic,
        IdentityProviderReadExtendedPublic,
    ],
)
def identity_provider_read_class(cls) -> Any:
    """IdentityProvider Read schema."""
    return cls
