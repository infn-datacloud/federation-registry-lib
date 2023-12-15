"""Provider specific fixtures."""
from typing import Any

from pytest_cases import fixture, parametrize

from app.provider.models import Provider
from app.provider.schemas import (
    ProviderBase,
    ProviderBasePublic,
    ProviderRead,
    ProviderReadPublic,
)
from app.provider.schemas_extended import (
    ProviderCreateExtended,
    ProviderReadExtended,
    ProviderReadExtendedPublic,
)
from tests.common.schema_validators import (
    BaseSchemaValidation,
    CreateSchemaValidation,
    ReadSchemaValidation,
)


@fixture
def provider_create_validator() -> (
    CreateSchemaValidation[ProviderBase, ProviderBasePublic, ProviderCreateExtended]
):
    """Instance to validate provider create schemas."""
    return CreateSchemaValidation[
        ProviderBase, ProviderBasePublic, ProviderCreateExtended
    ](base=ProviderBase, base_public=ProviderBasePublic, create=ProviderCreateExtended)


@fixture
def provider_read_validator() -> (
    ReadSchemaValidation[
        ProviderBase,
        ProviderBasePublic,
        ProviderRead,
        ProviderReadPublic,
        ProviderReadExtended,
        ProviderReadExtendedPublic,
        Provider,
    ]
):
    """Instance to validate provider read schemas."""
    return ReadSchemaValidation[
        ProviderBase,
        ProviderBasePublic,
        ProviderRead,
        ProviderReadPublic,
        ProviderReadExtended,
        ProviderReadExtendedPublic,
        Provider,
    ](
        base=ProviderBase,
        base_public=ProviderBasePublic,
        read=ProviderRead,
        read_extended=ProviderReadExtended,
    )


@fixture
def provider_patch_validator() -> (
    BaseSchemaValidation[ProviderBase, ProviderBasePublic]
):
    """Instance to validate provider patch schemas."""
    return BaseSchemaValidation[ProviderBase, ProviderBasePublic](
        base=ProviderBase, base_public=ProviderBasePublic
    )


@fixture
@parametrize(
    cls={
        ProviderRead,
        ProviderReadExtended,
        ProviderReadPublic,
        ProviderReadExtendedPublic,
    },
)
def provider_read_class(cls) -> Any:
    """Provider Read schema."""
    return cls
