"""Location specific cases."""
from typing import Any, Dict, Tuple, Type, Union

from pytest_cases import case, parametrize

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
from tests.common.utils import detect_public_extended_details


@case(tags="create_valid")
def case_location_create_valid_schema_actors(
    location_create_valid_data: Dict[str, Any],
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


@case(tags="create_invalid")
def case_location_create_invalid_schema_actors(
    location_create_invalid_data: Dict[str, Any],
) -> Tuple[Type[LocationCreate], Dict[str, Any]]:
    """Fixture with the create class and the invalid data to validate."""
    return LocationCreate, location_create_invalid_data


@case(tags="patch_valid")
def case_location_patch_valid_schema_actors(
    location_patch_valid_data: Dict[str, Any],
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


@case(tags="patch_invalid")
def case_location_patch_invalid_schema_actors(
    location_patch_invalid_data: Dict[str, Any],
) -> Tuple[Type[LocationUpdate], Dict[str, Any]]:
    """Fixture with the update class and the invalid data to validate."""
    return LocationUpdate, location_patch_invalid_data


@case(tags="read")
@parametrize(
    cls=[
        LocationRead,
        LocationReadExtended,
        LocationReadPublic,
        LocationReadExtendedPublic,
    ]
)
def case_location_valid_read_schema_tuple(
    cls: Union[
        LocationRead,
        LocationReadPublic,
        LocationReadExtended,
        LocationReadExtendedPublic,
    ],
    db_location: Location,
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
    bool,
    bool,
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
    is_public, is_extended = detect_public_extended_details(cls)
    return cls, validator, db_location, is_public, is_extended
