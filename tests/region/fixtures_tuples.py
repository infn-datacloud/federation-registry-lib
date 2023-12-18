"""Region specific fixtures."""
from typing import Any, Dict, Tuple, Type, Union

from pytest_cases import fixture

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
from tests.common.schema_validators import (
    CreateSchemaValidation,
    PatchSchemaValidation,
    ReadSchemaValidation,
)


@fixture
def region_valid_create_schema_tuple(
    region_create_validator, region_create_valid_data
) -> Tuple[
    Type[RegionCreateExtended],
    CreateSchemaValidation[RegionBase, RegionBasePublic, RegionCreateExtended],
    Dict[str, Any],
]:
    """Fixture with the create class, validator and data to validate."""
    return RegionCreateExtended, region_create_validator, region_create_valid_data


@fixture
def region_invalid_create_schema_tuple(
    region_create_invalid_data,
) -> Tuple[Type[RegionCreateExtended], Dict[str, Any]]:
    """Fixture with the create class and the invalid data to validate."""
    return RegionCreateExtended, region_create_invalid_data


@fixture
def region_valid_patch_schema_tuple(
    region_patch_validator, region_patch_valid_data
) -> Tuple[
    Type[RegionUpdate],
    PatchSchemaValidation[RegionBase, RegionBasePublic],
    Dict[str, Any],
]:
    """Fixture with the update class, validator and data to validate."""
    return RegionUpdate, region_patch_validator, region_patch_valid_data


@fixture
def region_invalid_patch_schema_tuple(
    region_patch_invalid_data,
) -> Tuple[Type[RegionUpdate], Dict[str, Any]]:
    """Fixture with the update class and the invalid data to validate."""
    return RegionUpdate, region_patch_invalid_data


@fixture
def region_valid_read_schema_tuple(
    region_read_class, region_read_validator, db_region
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
    return region_read_class, region_read_validator, db_region
