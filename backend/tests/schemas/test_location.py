import pytest
from app.location.models import Location
from app.location.schemas import LocationRead, LocationReadPublic, LocationReadShort
from app.location.schemas_extended import (
    LocationReadExtended,
    LocationReadExtendedPublic,
)
from pydantic import ValidationError
from tests.utils.location import (
    create_random_location,
    validate_read_extended_location_attrs,
    validate_read_extended_public_location_attrs,
    validate_read_location_attrs,
    validate_read_public_location_attrs,
    validate_read_short_location_attrs,
)
from tests.utils.utils import random_lower_string


def test_create_schema():
    """Create a valid 'Create' Schema."""
    create_random_location()
    create_random_location(default=True)


def test_invalid_create_schema():
    """List all invalid situations for a 'Create' Schema."""
    a = create_random_location()
    with pytest.raises(ValidationError):
        a.site = None
    with pytest.raises(ValidationError):
        a.country = None
    with pytest.raises(ValidationError):
        a.country = random_lower_string()
    with pytest.raises(ValidationError):
        # Latitude lower then minimum allowed value
        a.latitude = -200
    with pytest.raises(ValidationError):
        # Latitude greater then maximum allowed value
        a.latitude = 200
    with pytest.raises(ValidationError):
        # Longitude lower then minimum allowed value
        a.longitude = -100
    with pytest.raises(ValidationError):
        # Longitude greater then maximum allowed value
        a.longitude = 100


def test_read_schema_with_single_region(db_location: Location):
    """Create a valid 'Read' Schema from DB object.

    Apply conversion for this item for all read schemas. No one of them should raise
    errors.

    Target location is linked to a single region.
    """
    schema = LocationRead.from_orm(db_location)
    validate_read_location_attrs(obj_out=schema, db_item=db_location)
    schema = LocationReadShort.from_orm(db_location)
    validate_read_short_location_attrs(obj_out=schema, db_item=db_location)
    schema = LocationReadPublic.from_orm(db_location)
    validate_read_public_location_attrs(obj_out=schema, db_item=db_location)
    schema = LocationReadExtended.from_orm(db_location)
    validate_read_extended_location_attrs(obj_out=schema, db_item=db_location)
    schema = LocationReadExtendedPublic.from_orm(db_location)
    validate_read_extended_public_location_attrs(obj_out=schema, db_item=db_location)


def test_read_schema_with_multiple_regions(db_location_with_multiple_regions: Location):
    """Create a valid 'Read' Schema from DB object.

    Apply conversion for this item for all read schemas. No one of them should raise
    errors.

    Target location is linked to multiple regions.
    """
    schema = LocationRead.from_orm(db_location_with_multiple_regions)
    validate_read_location_attrs(
        obj_out=schema, db_item=db_location_with_multiple_regions
    )
    schema = LocationReadShort.from_orm(db_location_with_multiple_regions)
    validate_read_short_location_attrs(
        obj_out=schema, db_item=db_location_with_multiple_regions
    )
    schema = LocationReadPublic.from_orm(db_location_with_multiple_regions)
    validate_read_public_location_attrs(
        obj_out=schema, db_item=db_location_with_multiple_regions
    )
    schema = LocationReadExtended.from_orm(db_location_with_multiple_regions)
    assert len(schema.regions) > 1
    validate_read_extended_location_attrs(
        obj_out=schema, db_item=db_location_with_multiple_regions
    )
    schema = LocationReadExtendedPublic.from_orm(db_location_with_multiple_regions)
    assert len(schema.regions) > 1
    validate_read_extended_public_location_attrs(
        obj_out=schema, db_item=db_location_with_multiple_regions
    )
