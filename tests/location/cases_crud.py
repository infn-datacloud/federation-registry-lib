"""Location specific fixtures."""
from typing import Any, Dict, List, Optional, Tuple

from pytest_cases import case, parametrize

from app.location.crud import CRUDLocation, location_mng
from app.location.models import Location
from app.location.schemas import (
    LocationBase,
    LocationBasePublic,
    LocationCreate,
    LocationUpdate,
)
from app.region.models import Region
from tests.common.crud.validators import (
    CreateOperationValidation,
    DeleteOperationValidation,
    PatchOperationValidation,
    ReadOperationValidation,
)
from tests.location.fixtures_patch_dict import (
    location_patch_not_equal_data,
)

location_get_attr = [*LocationBase.__fields__.keys(), "uid", None]
location_sort_attr = [*LocationBase.__fields__.keys(), "uid"]
location_patch_attr = [*LocationBase.__fields__.keys()]
location_patch_default_attr = [
    k for k, v in LocationBase.__fields__.items() if not v.required
]
location_patch_required_attr = [
    k for k, v in LocationBase.__fields__.items() if v.required
]


@case(tags=["location", "not_existing"])
def case_location_not_existing_actors() -> CRUDLocation:
    """Return location manager."""
    return location_mng


@case(tags=["location", "create_item"])
def case_location_create_item_actors(
    location_create_valid_data: Dict[str, Any], db_region_simple: Region
) -> Tuple[
    CRUDLocation,
    CreateOperationValidation[
        LocationBase, LocationBasePublic, LocationCreate, Location
    ],
    LocationCreate,
    Dict[str, Any],
    List[str],
]:
    """Fixture with the create class, validator and data to validate."""
    validator = CreateOperationValidation[
        LocationBase, LocationBasePublic, LocationCreate, Location
    ](base=LocationBase, base_public=LocationBasePublic, create=LocationCreate)
    return (
        location_mng,
        validator,
        LocationCreate(**location_create_valid_data),
        {"region": db_region_simple},
        ["regions"],
    )


@case(tags=["location", "read_single"])
@parametrize(attr=location_get_attr)
def case_location_read_item_actors(
    db_location_no_defaults: Location, attr: str
) -> Tuple[
    CRUDLocation,
    ReadOperationValidation[LocationBase, LocationBasePublic, Location],
    Location,
    str,
]:
    """Fixture with the read class, validator and the db item to read."""
    validator = ReadOperationValidation[LocationBase, LocationBasePublic, Location](
        base=LocationBase, base_public=LocationBasePublic
    )
    return location_mng, validator, db_location_no_defaults, attr


@case(tags=["location", "read_multi"])
@parametrize(attr=location_get_attr)
def case_location_read_items_actors(
    db_location_simple: Location, db_location_no_defaults: Location, attr: str
) -> Tuple[
    CRUDLocation,
    ReadOperationValidation[LocationBase, LocationBasePublic, Location],
    Location,
    str,
]:
    """Fixture with the read class, validator and the db items to read."""
    validator = ReadOperationValidation[LocationBase, LocationBasePublic, Location](
        base=LocationBase, base_public=LocationBasePublic
    )
    return (
        location_mng,
        validator,
        [db_location_no_defaults, db_location_simple],
        attr,
    )


@case(tags=["location", "sort"])
@parametrize(reverse=[True, False])
@parametrize(attr=location_sort_attr)
def case_location_read_items_sort(
    db_location_simple: Location,
    db_location_no_defaults: Location,
    reverse: bool,
    attr: str,
) -> Tuple[
    CRUDLocation,
    ReadOperationValidation[LocationBase, LocationBasePublic, Location],
    Location,
    str,
]:
    """Fixture with the read class, validator and the db item to read."""
    validator = ReadOperationValidation[LocationBase, LocationBasePublic, Location](
        base=LocationBase, base_public=LocationBasePublic
    )
    if reverse:
        attr = "-" + attr
    return (
        location_mng,
        validator,
        [db_location_no_defaults, db_location_simple],
        attr,
    )


@case(tags=["location", "skip"])
@parametrize(skip=[0, 1, 2])
def case_location_read_items_skip(
    db_location_simple: Location, db_location_no_defaults: Location, skip: int
) -> Tuple[
    CRUDLocation,
    ReadOperationValidation[LocationBase, LocationBasePublic, Location],
    Location,
    str,
]:
    """Fixture with the read class, validator and the db item to read."""
    validator = ReadOperationValidation[LocationBase, LocationBasePublic, Location](
        base=LocationBase, base_public=LocationBasePublic
    )
    return (
        location_mng,
        validator,
        [db_location_no_defaults, db_location_simple],
        skip,
    )


@case(tags=["location", "limit"])
@parametrize(limit=[None, 0, 1, 2, 3])
def case_location_read_items_limit(
    db_location_simple: Location,
    db_location_no_defaults: Location,
    limit: Optional[int],
) -> Tuple[
    CRUDLocation,
    ReadOperationValidation[LocationBase, LocationBasePublic, Location],
    Location,
    str,
]:
    """Fixture with the read class, validator and the db item to read."""
    validator = ReadOperationValidation[LocationBase, LocationBasePublic, Location](
        base=LocationBase, base_public=LocationBasePublic
    )
    return (
        location_mng,
        validator,
        [db_location_no_defaults, db_location_simple],
        limit,
    )


@case(tags=["location", "delete"])
def case_location_delete_item_actors(
    db_location: Location,
) -> Tuple[
    CRUDLocation,
    DeleteOperationValidation[LocationBase, LocationBasePublic, Location],
    Location,
]:
    """Fixture with the delete class, validator and the db items to read."""
    validator = DeleteOperationValidation[LocationBase, LocationBasePublic, Location](
        base=LocationBase, base_public=LocationBasePublic, managers={}
    )
    return location_mng, validator, db_location


@case(tags=["location", "patch"])
def case_location_patch_item_actors(
    db_location_simple: Location, location_patch_valid_data: Dict[str, Any]
) -> Tuple[
    CRUDLocation,
    PatchOperationValidation[LocationBase, LocationBasePublic, Location],
    Location,
    LocationUpdate,
]:
    """Fixture with the delete class, validator and the db items to read."""
    validator = PatchOperationValidation[LocationBase, LocationBasePublic, Location](
        base=LocationBase, base_public=LocationBasePublic
    )
    new_data = location_patch_not_equal_data(
        db_item=db_location_simple, new_data=location_patch_valid_data
    )
    return location_mng, validator, db_location_simple, LocationUpdate(**new_data)


@case(tags=["location", "patch"])
@parametrize(attr=location_patch_default_attr)
def case_location_patch_item_with_default_actors(
    db_location_no_defaults: Location, attr: str
) -> Tuple[CRUDLocation, Location, LocationUpdate]:
    """Fixture with the delete class, validator and the db items to read."""
    validator = PatchOperationValidation[LocationBase, LocationBasePublic, Location](
        base=LocationBase, base_public=LocationBasePublic
    )
    field_data = LocationUpdate.__fields__.get(attr)
    location_patch_valid_data = {attr: field_data.get_default()}
    return (
        location_mng,
        validator,
        db_location_no_defaults,
        LocationUpdate(**location_patch_valid_data),
    )


@case(tags=["location", "patch_required_with_none"])
@parametrize(attr=location_patch_required_attr)
def case_location_patch_item_required_with_none_actors(
    db_location_no_defaults: Location, attr: str
) -> Tuple[CRUDLocation, Location, LocationUpdate]:
    """Fixture with the delete class, validator and the db items to read."""
    field_data = LocationUpdate.__fields__.get(attr)
    location_patch_valid_data = {attr: field_data.get_default()}
    return (
        location_mng,
        db_location_no_defaults,
        LocationUpdate(**location_patch_valid_data),
    )


@case(tags=["location", "patch_no_changes"])
@parametrize(attr=location_patch_attr)
def case_location_patch_item_no_changes_actors(
    db_location_simple: Location, attr: str
) -> Tuple[CRUDLocation, Location, LocationUpdate]:
    """Fixture with the delete class, validator and the db items to read."""
    location_patch_valid_data = {attr: db_location_simple.__getattribute__(attr)}
    return (
        location_mng,
        db_location_simple,
        LocationUpdate(**location_patch_valid_data),
    )
