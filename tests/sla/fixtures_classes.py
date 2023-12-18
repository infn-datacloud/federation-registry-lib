"""SLA specific fixtures."""
from typing import Any

from pytest_cases import fixture, parametrize

from app.provider.schemas_extended import SLACreateExtended
from app.sla.models import SLA
from app.sla.schemas import (
    SLABase,
    SLABasePublic,
    SLARead,
    SLAReadPublic,
)
from app.sla.schemas_extended import SLAReadExtended, SLAReadExtendedPublic
from tests.common.schemas.validators import (
    CreateSchemaValidation,
    PatchSchemaValidation,
    ReadSchemaValidation,
)


@fixture
def sla_create_validator() -> (
    CreateSchemaValidation[SLABase, SLABasePublic, SLACreateExtended]
):
    """Instance to validate sla create schemas."""
    return CreateSchemaValidation[SLABase, SLABasePublic, SLACreateExtended](
        base=SLABase, base_public=SLABasePublic, create=SLACreateExtended
    )


@fixture
def sla_read_validator() -> (
    ReadSchemaValidation[
        SLABase,
        SLABasePublic,
        SLARead,
        SLAReadPublic,
        SLAReadExtended,
        SLAReadExtendedPublic,
        SLA,
    ]
):
    """Instance to validate sla read schemas."""
    return ReadSchemaValidation[
        SLABase,
        SLABasePublic,
        SLARead,
        SLAReadPublic,
        SLAReadExtended,
        SLAReadExtendedPublic,
        SLA,
    ](
        base=SLABase,
        base_public=SLABasePublic,
        read=SLARead,
        read_extended=SLAReadExtended,
    )


@fixture
def sla_patch_validator() -> PatchSchemaValidation[SLABase, SLABasePublic]:
    """Instance to validate sla patch schemas."""
    return PatchSchemaValidation[SLABase, SLABasePublic](
        base=SLABase, base_public=SLABasePublic
    )


@fixture
@parametrize(cls=[SLARead, SLAReadExtended, SLAReadPublic, SLAReadExtendedPublic])
def sla_read_class(cls) -> Any:
    """SLA Read schema."""
    return cls
