"""Region specific cases."""
from typing import Any, Dict, Tuple, Type, Union

from pytest_cases import case, parametrize

from app.provider.schemas_extended import (
    RegionCreateExtended,
)
from app.region.models import Region
from app.region.schemas import (
    RegionBase,
    RegionBasePublic,
    RegionRead,
    RegionReadPublic,
    RegionUpdate,
)
from app.region.schemas_extended import RegionReadExtended, RegionReadExtendedPublic
from tests.common.schemas.validators import (
    CreateSchemaValidation,
    PatchSchemaValidation,
    ReadSchemaValidation,
)


@case(tags="create_valid")
def case_region_create_valid_schema_actors(
    region_create_valid_data: Dict[str, Any],
) -> Tuple[
    Type[RegionCreateExtended],
    CreateSchemaValidation[RegionBase, RegionBasePublic, RegionCreateExtended],
    Dict[str, Any],
]:
    """Fixture with the create class, validator and data to validate."""
    validator = CreateSchemaValidation[
        RegionBase, RegionBasePublic, RegionCreateExtended
    ](base=RegionBase, base_public=RegionBasePublic, create=RegionCreateExtended)
    return RegionCreateExtended, validator, region_create_valid_data


@case(tags="create_invalid")
def case_region_create_invalid_schema_actors(
    region_create_invalid_data: Dict[str, Any],
) -> Tuple[Type[RegionCreateExtended], Dict[str, Any]]:
    """Fixture with the create class and the invalid data to validate."""
    return RegionCreateExtended, region_create_invalid_data


@case(tags="patch_valid")
def case_region_patch_valid_schema_actors(
    region_patch_valid_data: Dict[str, Any],
) -> Tuple[
    Type[RegionUpdate],
    PatchSchemaValidation[RegionBase, RegionBasePublic],
    Dict[str, Any],
]:
    """Fixture with the update class, validator and data to validate."""
    validator = PatchSchemaValidation[RegionBase, RegionBasePublic](
        base=RegionBase, base_public=RegionBasePublic
    )
    return RegionUpdate, validator, region_patch_valid_data


@case(tags="patch_invalid")
def case_region_patch_invalid_schema_actors(
    region_patch_invalid_data: Dict[str, Any],
) -> Tuple[Type[RegionUpdate], Dict[str, Any]]:
    """Fixture with the update class and the invalid data to validate."""
    return RegionUpdate, region_patch_invalid_data


@case(tags="read")
@parametrize(
    cls=[RegionRead, RegionReadPublic, RegionReadExtended, RegionReadExtendedPublic]
)
def case_region_valid_read_schema_tuple(
    cls: Union[
        RegionRead, RegionReadPublic, RegionReadExtended, RegionReadExtendedPublic
    ],
    db_region: Region,
) -> Tuple[
    Union[RegionRead, RegionReadPublic, RegionReadExtended, RegionReadExtendedPublic],
    ReadSchemaValidation[
        RegionBase,
        RegionBasePublic,
        RegionRead,
        RegionReadPublic,
        RegionReadExtended,
        RegionReadExtendedPublic,
        Region,
    ],
    Region,
]:
    """Fixture with the read class, validator and the db item to read."""
    validator = ReadSchemaValidation[
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
    cls_name = cls.__name__
    is_public = False
    is_extended = False
    if "Public" in cls_name:
        is_public = True
    if "Extended" in cls_name:
        is_extended = True
    return cls, validator, db_region, is_public, is_extended
