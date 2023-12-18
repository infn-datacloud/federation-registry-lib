"""Flavor specific fixtures."""
from typing import Any

from pytest_cases import fixture, parametrize

from app.flavor.models import Flavor
from app.flavor.schemas import (
    FlavorBase,
    FlavorBasePublic,
    FlavorRead,
    FlavorReadPublic,
)
from app.flavor.schemas_extended import FlavorReadExtended, FlavorReadExtendedPublic
from app.provider.schemas_extended import FlavorCreateExtended
from tests.common.schema_validators import (
    CreateSchemaValidation,
    PatchSchemaValidation,
    ReadSchemaValidation,
)


@fixture
def flavor_create_validator() -> (
    CreateSchemaValidation[FlavorBase, FlavorBasePublic, FlavorCreateExtended]
):
    """Instance to validate flavor create schemas."""
    return CreateSchemaValidation[FlavorBase, FlavorBasePublic, FlavorCreateExtended](
        base=FlavorBase, base_public=FlavorBasePublic, create=FlavorCreateExtended
    )


@fixture
def flavor_read_validator() -> (
    ReadSchemaValidation[
        FlavorBase,
        FlavorBasePublic,
        FlavorRead,
        FlavorReadPublic,
        FlavorReadExtended,
        FlavorReadExtendedPublic,
        Flavor,
    ]
):
    """Instance to validate flavor read schemas."""
    return ReadSchemaValidation[
        FlavorBase,
        FlavorBasePublic,
        FlavorRead,
        FlavorReadPublic,
        FlavorReadExtended,
        FlavorReadExtendedPublic,
        Flavor,
    ](
        base=FlavorBase,
        base_public=FlavorBasePublic,
        read=FlavorRead,
        read_extended=FlavorReadExtended,
    )


@fixture
def flavor_patch_validator() -> PatchSchemaValidation[FlavorBase, FlavorBasePublic]:
    """Instance to validate flavor patch schemas."""
    return PatchSchemaValidation[FlavorBase, FlavorBasePublic](
        base=FlavorBase, base_public=FlavorBasePublic
    )


@fixture
@parametrize(
    cls=[FlavorRead, FlavorReadExtended, FlavorReadPublic, FlavorReadExtendedPublic]
)
def flavor_read_class(cls) -> Any:
    """Flavor Read schema."""
    return cls
