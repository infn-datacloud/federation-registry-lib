"""Location specific fixtures."""
from typing import Any

from pytest_cases import fixture, parametrize

from app.location.models import Location
from app.location.schemas import (
    LocationBase,
    LocationBasePublic,
    LocationRead,
    LocationReadPublic,
)
from app.location.schemas_extended import (
    LocationReadExtended,
    LocationReadExtendedPublic,
)
from app.provider.schemas_extended import LocationCreate
from tests.common.schema_validators import (
    BaseSchemaValidation,
    CreateSchemaValidation,
    ReadSchemaValidation,
)


@fixture
def location_create_validator() -> (
    CreateSchemaValidation[LocationBase, LocationBasePublic, LocationCreate]
):
    """Instance to validate location create schemas."""
    return CreateSchemaValidation[LocationBase, LocationBasePublic, LocationCreate](
        base=LocationBase, base_public=LocationBasePublic, create=LocationCreate
    )


@fixture
def location_read_validator() -> (
    ReadSchemaValidation[
        LocationBase,
        LocationBasePublic,
        LocationRead,
        LocationReadPublic,
        LocationReadExtended,
        LocationReadExtendedPublic,
        Location,
    ]
):
    """Instance to validate location read schemas."""
    return ReadSchemaValidation[
        LocationBase,
        LocationBasePublic,
        LocationRead,
        LocationReadPublic,
        LocationReadExtended,
        LocationReadExtendedPublic,
        Location,
    ](
        base=LocationBase,
        base_public=LocationBasePublic,
        read=LocationRead,
        read_extended=LocationReadExtended,
    )


@fixture
def location_patch_validator() -> (
    BaseSchemaValidation[LocationBase, LocationBasePublic]
):
    """Instance to validate location patch schemas."""
    return BaseSchemaValidation[LocationBase, LocationBasePublic](
        base=LocationBase, base_public=LocationBasePublic
    )


@fixture
@parametrize(
    cls=[
        LocationRead,
        LocationReadExtended,
        LocationReadPublic,
        LocationReadExtendedPublic,
    ]
)
def location_read_class(cls) -> Any:
    """Location Read schema."""
    return cls
