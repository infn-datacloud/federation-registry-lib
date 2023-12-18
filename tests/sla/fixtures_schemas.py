"""SLA specific fixtures."""
from typing import Any, Dict, Tuple, Type, Union

from pytest_cases import fixture, parametrize

from app.provider.schemas_extended import SLACreateExtended
from app.sla.models import SLA
from app.sla.schemas import (
    SLABase,
    SLABasePublic,
    SLARead,
    SLAReadPublic,
    SLAUpdate,
)
from app.sla.schemas_extended import SLAReadExtended, SLAReadExtendedPublic
from tests.common.schemas.validators import (
    CreateSchemaValidation,
    PatchSchemaValidation,
    ReadSchemaValidation,
)


@fixture
@parametrize(cls=[SLARead, SLAReadExtended, SLAReadPublic, SLAReadExtendedPublic])
def sla_read_class(cls) -> Any:
    """SLA Read schema."""
    return cls


@fixture
def sla_valid_create_schema_tuple(
    sla_create_valid_data,
) -> Tuple[
    Type[SLACreateExtended],
    CreateSchemaValidation[SLABase, SLABasePublic, SLACreateExtended],
    Dict[str, Any],
]:
    """Fixture with the create class, validator and data to validate."""
    validator = CreateSchemaValidation[SLABase, SLABasePublic, SLACreateExtended](
        base=SLABase, base_public=SLABasePublic, create=SLACreateExtended
    )
    return SLACreateExtended, validator, sla_create_valid_data


@fixture
def sla_invalid_create_schema_tuple(
    sla_create_invalid_data,
) -> Tuple[Type[SLACreateExtended], Dict[str, Any]]:
    """Fixture with the create class and the invalid data to validate."""
    return SLACreateExtended, sla_create_invalid_data


@fixture
def sla_valid_patch_schema_tuple(
    sla_patch_valid_data,
) -> Tuple[
    Type[SLAUpdate],
    PatchSchemaValidation[SLABase, SLABasePublic],
    Dict[str, Any],
]:
    """Fixture with the update class, validator and data to validate."""
    validator = PatchSchemaValidation[SLABase, SLABasePublic](
        base=SLABase, base_public=SLABasePublic
    )
    return SLAUpdate, validator, sla_patch_valid_data


@fixture
def sla_invalid_patch_schema_tuple(
    sla_patch_invalid_data,
) -> Tuple[Type[SLAUpdate], Dict[str, Any]]:
    """Fixture with the update class and the invalid data to validate."""
    return SLAUpdate, sla_patch_invalid_data


@fixture
def sla_valid_read_schema_tuple(
    sla_read_class, db_sla
) -> Tuple[
    Union[SLARead, SLAReadPublic, SLAReadExtended, SLAReadExtendedPublic],
    ReadSchemaValidation[
        SLABase,
        SLABasePublic,
        SLARead,
        SLAReadPublic,
        SLAReadExtended,
        SLAReadExtendedPublic,
        SLA,
    ],
    SLA,
]:
    """Fixture with the read class, validator and the db item to read."""
    validator = ReadSchemaValidation[
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
    return sla_read_class, validator, db_sla
