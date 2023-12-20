"""SLA specific cases."""
from typing import Any, Dict, Tuple, Type, Union

from pytest_cases import case, parametrize

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


@case(tags="create_valid")
def case_sla_create_valid_schema_actors(
    sla_create_valid_data: Dict[str, Any],
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


@case(tags="create_invalid")
def case_sla_create_invalid_schema_actors(
    sla_create_invalid_data: Dict[str, Any],
) -> Tuple[Type[SLACreateExtended], Dict[str, Any]]:
    """Fixture with the create class and the invalid data to validate."""
    return SLACreateExtended, sla_create_invalid_data


@case(tags="patch_valid")
def case_sla_patch_valid_schema_actors(
    sla_patch_valid_data: Dict[str, Any],
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


@case(tags="patch_invalid")
def case_sla_patch_invalid_schema_actors(
    sla_patch_invalid_data: Dict[str, Any],
) -> Tuple[Type[SLAUpdate], Dict[str, Any]]:
    """Fixture with the update class and the invalid data to validate."""
    return SLAUpdate, sla_patch_invalid_data


@case(tags="read")
@parametrize(cls=[SLARead, SLAReadExtended, SLAReadPublic, SLAReadExtendedPublic])
def case_sla_valid_read_schema_tuple(
    cls: Union[SLARead, SLAReadPublic, SLAReadExtended, SLAReadExtendedPublic],
    db_sla: SLA,
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
    cls_name = cls.__name__
    is_public = False
    is_extended = False
    if "Public" in cls_name:
        is_public = True
    if "Extended" in cls_name:
        is_extended = True
    return cls, validator, db_sla, is_public, is_extended
