"""Region specific fixtures."""
from typing import Any

from pytest_cases import fixture, parametrize

from app.provider.schemas_extended import (
    RegionCreateExtended,
)
from app.region.models import Region
from app.region.schemas import (
    RegionBase,
    RegionBasePublic,
    RegionRead,
    RegionReadPublic,
)
from app.region.schemas_extended import RegionReadExtended, RegionReadExtendedPublic
from tests.common.schema_validators import (
    BaseSchemaValidation,
    CreateSchemaValidation,
    ReadSchemaValidation,
)


@fixture
def region_create_validator() -> (
    CreateSchemaValidation[RegionBase, RegionBasePublic, RegionCreateExtended]
):
    """Instance to validate region create schemas."""
    return CreateSchemaValidation[RegionBase, RegionBasePublic, RegionCreateExtended](
        base=RegionBase, base_public=RegionBasePublic, create=RegionCreateExtended
    )


@fixture
def region_read_validator() -> (
    ReadSchemaValidation[
        RegionBase,
        RegionBasePublic,
        RegionRead,
        RegionReadPublic,
        RegionReadExtended,
        RegionReadExtendedPublic,
        Region,
    ]
):
    """Instance to validate region read schemas."""
    return ReadSchemaValidation[
        RegionBase,
        RegionBasePublic,
        RegionRead,
        RegionReadPublic,
        RegionReadExtended,
        RegionReadExtendedPublic,
        Region,
    ](
        base=RegionBase,
        base_public=RegionBasePublic,
        read=RegionRead,
        read_extended=RegionReadExtended,
    )


@fixture
def region_patch_validator() -> BaseSchemaValidation[RegionBase, RegionBasePublic]:
    """Instance to validate region patch schemas."""
    return BaseSchemaValidation[RegionBase, RegionBasePublic](
        base=RegionBase, base_public=RegionBasePublic
    )


@fixture
@parametrize(
    cls=[RegionRead, RegionReadExtended, RegionReadPublic, RegionReadExtendedPublic]
)
def region_read_class(cls) -> Any:
    """Region Read schema."""
    return cls
