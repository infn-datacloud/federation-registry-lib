import pytest
from neomodel import RelationshipManager, RequiredProperty
from pytest_cases import parametrize, parametrize_with_cases

from app.provider.models import Provider
from tests.common.utils import random_lower_string


class CaseMissing:
    @parametrize(value=["name", "type"])
    def case_missing(self, value: str) -> str:
        return value


def test_default_attr() -> None:
    d = {"name": random_lower_string(), "type": random_lower_string()}
    item = Provider(**d)
    assert item.uid is not None
    assert item.description == ""
    assert item.name == d.get("name")
    assert item.type == d.get("type")
    assert item.is_public is False
    assert item.status is None
    assert item.support_emails is None
    assert isinstance(item.projects, RelationshipManager)
    assert isinstance(item.regions, RelationshipManager)
    assert isinstance(item.identity_providers, RelationshipManager)


@parametrize_with_cases("missing_attr", cases=CaseMissing)
def test_missing_attr(missing_attr: str) -> None:
    d = {
        "name": None if missing_attr == "name" else random_lower_string(),
        "type": None if missing_attr == "type" else random_lower_string(),
    }
    item = Provider(**d)
    with pytest.raises(RequiredProperty):
        item.save()
