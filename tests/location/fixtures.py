"""Location specific fixtures."""
from typing import Any, Dict, Tuple, Type, Union

from pytest_cases import fixture, fixture_ref, parametrize

from app.location.crud import location_mng
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
from app.region.models import Region
from tests.common.schema_validators import (
    BaseSchemaValidation,
    CreateSchemaValidation,
    ReadSchemaValidation,
)
from tests.utils.location import random_country, random_latitude, random_longitude
from tests.utils.utils import random_lower_string

invalid_create_key_values = {
    ("description", None),
    ("site", None),
    ("country", None),
    ("country", random_lower_string()),
    ("latitude", -181),
    ("latitude", 181),
    ("longitude", -91),
    ("longitude", 91),
}
patch_key_values = {
    ("description", random_lower_string()),
    ("site", random_lower_string()),
    ("country", random_country()),
    ("latitude", random_latitude()),
    ("longitude", random_longitude()),
}
invalid_patch_key_values = {  # None is not accepted because there is a default
    ("description", None),
    ("country", random_lower_string()),
    ("latitude", -181),
    ("latitude", 181),
    ("longitude", -91),
    ("longitude", 91),
}
relationships_num = {0, 1, 2}


# CLASSES FIXTURES


@fixture(scope="package")
def location_create_validator() -> (
    CreateSchemaValidation[LocationBase, LocationBasePublic, LocationCreate]
):
    """Instance to validate location create schemas."""
    return CreateSchemaValidation[LocationBase, LocationBasePublic, LocationCreate](
        base=LocationBase, base_public=LocationBasePublic, create=LocationCreate
    )


@fixture(scope="package")
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


@fixture(scope="package")
def location_patch_validator() -> (
    BaseSchemaValidation[LocationBase, LocationBasePublic]
):
    """Instance to validate location patch schemas."""
    return BaseSchemaValidation[LocationBase, LocationBasePublic](
        base=LocationBase, base_public=LocationBasePublic
    )


@fixture(scope="package")
@parametrize(
    "cls",
    {
        LocationRead,
        LocationReadExtended,
        LocationReadPublic,
        LocationReadExtendedPublic,
    },
)
def location_read_class(cls) -> Any:
    """Location Read schema."""
    return cls


# DICT FIXTURES CREATE


@fixture
def location_create_mandatory_data() -> Dict[str, Any]:
    """Dict with Location mandatory attributes."""
    return {"site": random_lower_string(), "country": random_country()}


@fixture
def location_create_all_data(
    location_create_mandatory_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with all Location attributes."""
    return {
        **location_create_mandatory_data,
        "description": random_lower_string(),
        "latitude": random_latitude(),
        "longitude": random_longitude(),
    }


@fixture
@parametrize(
    "data",
    {
        fixture_ref("location_create_mandatory_data"),
        fixture_ref("location_create_all_data"),
    },
)
def location_create_valid_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Valid set of attributes for a Location patch schema."""
    return data


@fixture
@parametrize("k, v", invalid_create_key_values)
def location_create_invalid_pair(
    location_create_mandatory_data: Dict[str, Any], k: str, v: Any
) -> Dict[str, Any]:
    """Dict with one invalid key-value pair."""
    data = {**location_create_mandatory_data}
    data[k] = v
    return data


@fixture
@parametrize("data", {fixture_ref("location_create_invalid_pair")})
def location_create_invalid_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Invalid set of attributes for a Location create schema."""
    return data


# DICT FIXTURES CREATE


@fixture
@parametrize("k, v", patch_key_values)
def location_patch_valid_data_single_attr(k: str, v: Any) -> Dict[str, Any]:
    """Valid set of single key-value pair for a Location patch schema."""
    return {k: v}


@fixture
@parametrize("data", {fixture_ref("location_patch_valid_data_single_attr")})
def location_patch_valid_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Valid set of attributes for a Location patch schema."""
    return data


@fixture
@parametrize("k, v", invalid_patch_key_values)
def location_patch_invalid_data(k: str, v: Any) -> Dict[str, Any]:
    """Invalid set of attributes for a Location patch schema."""
    return {k: v}


# DB INSTANCES FIXTURES


@fixture
def db_location_simple(
    location_create_mandatory_data: Dict[str, Any], db_region: Region
) -> Location:
    """Fixture with standard DB Location."""
    item = LocationCreate(**location_create_mandatory_data)
    return location_mng.create(obj_in=item, region=db_region)


@fixture
def db_shared_location(
    location_create_mandatory_data: Dict[str, Any],
    db_location_simple: Location,
    db_region2: Region,
    db_region3: Region,
) -> Location:
    """Location shared within multiple regions.

    This location is shared between regions belonging to the same providers and regions
    belonging to another provider.
    """
    d = {}
    for k in location_create_mandatory_data.keys():
        d[k] = db_location_simple.__getattribute__(k)
    item = LocationCreate(**d)
    location_mng.create(obj_in=item, region=db_region2)
    return location_mng.create(obj_in=item, region=db_region3)


@fixture
@parametrize(
    "db_item", {fixture_ref("db_location_simple"), fixture_ref("db_shared_location")}
)
def db_location(db_item: Location) -> Location:
    """Generic DB Location instance."""
    return db_item


# TUPLE FOR CASES FIXTURES


@fixture
def location_valid_create_schema_tuple(
    location_create_validator, location_create_valid_data
) -> Tuple[
    Type[LocationCreate],
    CreateSchemaValidation[LocationBase, LocationBasePublic, LocationCreate],
    Dict[str, Any],
]:
    """Fixture with the create class, validator and data to validate."""
    return LocationCreate, location_create_validator, location_create_valid_data


@fixture
def location_invalid_create_schema_tuple(
    location_create_invalid_data,
) -> Tuple[Type[LocationCreate], Dict[str, Any]]:
    """Fixture with the create class and the invalid data to validate."""
    return LocationCreate, location_create_invalid_data


@fixture
def location_valid_patch_schema_tuple(
    location_patch_validator, location_patch_valid_data
) -> Tuple[
    Type[LocationUpdate],
    BaseSchemaValidation[LocationBase, LocationBasePublic],
    Dict[str, Any],
]:
    """Fixture with the update class, validator and data to validate."""
    return LocationUpdate, location_patch_validator, location_patch_valid_data


@fixture
def location_invalid_patch_schema_tuple(
    location_patch_invalid_data,
) -> Tuple[Type[LocationUpdate], Dict[str, Any]]:
    """Fixture with the update class and the invalid data to validate."""
    return LocationUpdate, location_patch_invalid_data


@fixture
def location_valid_read_schema_tuple(
    location_read_class, location_read_validator, db_location
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
    return location_read_class, location_read_validator, db_location
