import pytest
from app.tests.utils.project import create_random_project
from pydantic import ValidationError


def test_create_schema():
    create_random_project()
    create_random_project(default=True)


def test_invalid_create_schema():
    a = create_random_project()
    with pytest.raises(ValidationError):
        a.uuid = None
    with pytest.raises(ValidationError):
        a.name = None
