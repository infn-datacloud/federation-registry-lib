import pytest
from app.tests.utils.network import create_random_network
from pydantic import ValidationError


def test_create_schema():
    create_random_network()
    create_random_network(default=True)
    create_random_network(is_shared=False)


def test_invalid_create_schema():
    a = create_random_network(is_shared=False)
    with pytest.raises(ValidationError):
        a.uuid = None
    with pytest.raises(ValidationError):
        a.name = None
    with pytest.raises(ValidationError):
        a.project = None
    with pytest.raises(ValidationError):
        a.is_shared = True
