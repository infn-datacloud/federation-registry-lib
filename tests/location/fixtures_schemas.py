"""Location specific fixtures."""
from typing import Any, Dict, Tuple, Type, Union

from pytest_cases import fixture, parametrize

from app.location.models import Location
from app.location.schemas import (
    LocationBase,
    LocationBasePublic,
    LocationRead,
    LocationReadPublic,
    LocationUpdate,
)
from app.location.schemas_extended import (
    LocationReadExtended,
    LocationReadExtendedPublic,
)
from app.provider.schemas_extended import LocationCreate
from tests.common.schemas.validators import (
    CreateSchemaValidation,
    PatchSchemaValidation,
    ReadSchemaValidation,
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


@fixture
def location_valid_create_schema_tuple(
    location_create_valid_data,
) -> Tuple[
    Type[LocationCreate],
    CreateSchemaValidation[LocationBase, LocationBasePublic, LocationCreate],
    Dict[str, Any],
]:
    """Fixture with the create class, validator and data to validate."""
    validator = CreateSchemaValidation[
        LocationBase, LocationBasePublic, LocationCreate
    ](base=LocationBase, base_public=LocationBasePublic, create=LocationCreate)
    return LocationCreate, validator, location_create_valid_data


@fixture
def location_invalid_create_schema_tuple(
    location_create_invalid_data,
) -> Tuple[Type[LocationCreate], Dict[str, Any]]:
    """Fixture with the create class and the invalid data to validate."""
    return LocationCreate, location_create_invalid_data


@fixture
def location_valid_patch_schema_tuple(
    location_patch_valid_data,
) -> Tuple[
    Type[LocationUpdate],
    PatchSchemaValidation[LocationBase, LocationBasePublic],
    Dict[str, Any],
]:
    """Fixture with the update class, validator and data to validate."""
    validator = PatchSchemaValidation[LocationBase, LocationBasePublic](
        base=LocationBase, base_public=LocationBasePublic
    )
    return LocationUpdate, validator, location_patch_valid_data


@fixture
def location_invalid_patch_schema_tuple(
    location_patch_invalid_data,
) -> Tuple[Type[LocationUpdate], Dict[str, Any]]:
    """Fixture with the update class and the invalid data to validate."""
    return LocationUpdate, location_patch_invalid_data


@fixture
def location_valid_read_schema_tuple(
    location_read_class, db_location
) -> Tuple[
    Union[
        LocationRead,
        LocationReadPublic,
        LocationReadExtended,
        LocationReadExtendedPublic,
    ],
    ReadSchemaValidation[
        LocationBase,
        LocationBasePublic,
        LocationRead,
        LocationReadPublic,
        LocationReadExtended,
        LocationReadExtendedPublic,
        Location,
    ],
    Location,
]:
    """Fixture with the read class, validator and the db item to read."""
    validator = ReadSchemaValidation[
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
    return location_read_class, validator, db_location
