import pytest
from app.tests.utils.user_group import create_random_user_group
from pydantic import ValidationError


def test_create_schema():
    create_random_user_group()
    create_random_user_group(default=True)


def test_invalid_create_schema():
    a = create_random_user_group()
    with pytest.raises(ValidationError):
        a.name = None
    with pytest.raises(ValidationError):
        a.slas = []
    with pytest.raises(ValidationError):
        a.slas = [a.slas[0], a.slas[0]]
