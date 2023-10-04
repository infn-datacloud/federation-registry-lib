import pytest
from app.tests.utils.flavor import create_random_flavor
from pydantic import ValidationError


def test_create_schema():
    create_random_flavor()
    create_random_flavor(default=True)
    create_random_flavor(is_public=False)


def test_invalid_create_schema():
    a = create_random_flavor(is_public=False)
    with pytest.raises(ValidationError):
        a.uuid = None
    with pytest.raises(ValidationError):
        a.name = None
    with pytest.raises(ValidationError):
        a.gpus = 0
    with pytest.raises(ValidationError):
        a.projects = []
    with pytest.raises(ValidationError):
        a.is_public = True
    with pytest.raises(ValidationError):
        a.projects = [a.projects[0], a.projects[0]]
