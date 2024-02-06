import pytest
from neomodel import RelationshipManager, RequiredProperty

from app.user_group.models import UserGroup
from tests.common.utils import random_lower_string


def test_default_attr() -> None:
    d = {"name": random_lower_string()}
    item = UserGroup(**d)
    assert item.uid is not None
    assert item.description == ""
    assert item.name == d.get("name")
    assert isinstance(item.identity_provider, RelationshipManager)
    assert isinstance(item.slas, RelationshipManager)


def test_missing_attr() -> None:
    item = UserGroup()
    with pytest.raises(RequiredProperty):
        item.save()
