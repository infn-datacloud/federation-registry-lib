import pytest
from app.location.crud import location
from app.location.schemas import LocationRead, LocationReadPublic, LocationReadShort
from app.location.schemas_extended import (
    LocationReadExtended,
    LocationReadExtendedPublic,
)
from app.region.models import Region
from pydantic import ValidationError
from tests.utils.location import create_random_location
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


def test_read_schema(db_region: Region):
    """Create a valid 'Read' Schema."""
    obj_in = create_random_location()
    db_obj = location.create(obj_in=obj_in, region=db_region)
    LocationRead.from_orm(db_obj)
    LocationReadPublic.from_orm(db_obj)
    LocationReadShort.from_orm(db_obj)
    LocationReadExtended.from_orm(db_obj)
    LocationReadExtendedPublic.from_orm(db_obj)

    obj_in = create_random_location(default=True)
    db_obj = location.update(db_obj=db_obj, obj_in=obj_in, force=True)
    LocationRead.from_orm(db_obj)
    LocationReadPublic.from_orm(db_obj)
    LocationReadShort.from_orm(db_obj)
    LocationReadExtended.from_orm(db_obj)
    LocationReadExtendedPublic.from_orm(db_obj)
