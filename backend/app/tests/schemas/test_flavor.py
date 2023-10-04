import pytest
from app.tests.utils.flavor import create_random_flavor
from pydantic import ValidationError


def test_create_schema():
    create_random_flavor()
    create_random_flavor(default=True)
    create_random_flavor(with_projects=True)


def test_invalid_schema():
    a = create_random_flavor(with_projects=True)
    with pytest.raises(ValidationError):
        a.gpus = 0
    with pytest.raises(ValidationError):
        a.projects = []
    with pytest.raises(ValidationError):
        a.is_public = True
    with pytest.raises(ValidationError):
        a.projects = [a.projects[0], a.projects[0]]
