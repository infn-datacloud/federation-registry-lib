import pytest
from app.tests.utils.image import create_random_image
from pydantic import ValidationError


def test_create_schema():
    create_random_image()
    create_random_image(default=True)
    create_random_image(is_public=False)


def test_invalid_create_schema():
    a = create_random_image(is_public=False)
    with pytest.raises(ValidationError):
        a.uuid = None
    with pytest.raises(ValidationError):
        a.name = None
    with pytest.raises(ValidationError):
        a.projects = []
    with pytest.raises(ValidationError):
        a.is_public = True
    with pytest.raises(ValidationError):
        a.projects = [a.projects[0], a.projects[0]]
