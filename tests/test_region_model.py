import pytest
from neomodel import RelationshipManager, RequiredProperty

from app.region.models import Region
from tests.common.utils import random_lower_string


def test_default_attr() -> None:
    d = {"name": random_lower_string()}
    item = Region(**d)
    assert item.uid is not None
    assert item.description == ""
    assert item.name == d.get("name")
    assert isinstance(item.location, RelationshipManager)
    assert isinstance(item.provider, RelationshipManager)
    assert isinstance(item.services, RelationshipManager)


def test_missing_attr() -> None:
    item = Region()
    with pytest.raises(RequiredProperty):
        item.save()
