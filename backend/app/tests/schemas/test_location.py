import pytest
from app.tests.utils.location import create_random_location
from pydantic import ValidationError


def test_create_schema():
    create_random_location()
    create_random_location(default=True)


def test_invalid_create_schema():
    a = create_random_location()
    with pytest.raises(ValidationError):
        a.site = None
    with pytest.raises(ValidationError):
        a.country = None
    with pytest.raises(ValidationError):
        a.latitude = -200
    with pytest.raises(ValidationError):
        a.latitude = 200
    with pytest.raises(ValidationError):
        a.longitude = -100
    with pytest.raises(ValidationError):
        a.longitude = 100
