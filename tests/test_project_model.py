from uuid import uuid4

import pytest
from neomodel import RelationshipManager, RequiredProperty
from pytest_cases import parametrize, parametrize_with_cases

from app.project.models import Project
from tests.common.utils import random_lower_string


class CaseMissing:
    @parametrize(value=["name", "uuid"])
    def case_missing(self, value: str) -> str:
        return value


def test_default_attr() -> None:
    d = {"name": random_lower_string(), "uuid": uuid4().hex}
    item = Project(**d)
    assert item.uid is not None
    assert item.description == ""
    assert item.name == d.get("name")
    assert item.uuid == d.get("uuid")
    assert isinstance(item.sla, RelationshipManager)
    assert isinstance(item.provider, RelationshipManager)
    assert isinstance(item.quotas, RelationshipManager)
    assert isinstance(item.private_flavors, RelationshipManager)
    assert isinstance(item.private_images, RelationshipManager)
    assert isinstance(item.private_networks, RelationshipManager)


@parametrize_with_cases("missing_attr", cases=CaseMissing)
def test_missing_attr(missing_attr: str) -> None:
    d = {
        "name": None if missing_attr == "name" else random_lower_string(),
        "uuid": None if missing_attr == "uuid" else uuid4().hex,
    }
    item = Project(**d)
    with pytest.raises(RequiredProperty):
        item.save()


# TODO test public_flavors
# TODO test public_images
# TODO test public_networks
