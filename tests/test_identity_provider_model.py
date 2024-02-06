import pytest
from neomodel import RelationshipManager, RequiredProperty
from pytest_cases import parametrize, parametrize_with_cases

from app.identity_provider.models import IdentityProvider
from tests.common.utils import random_lower_string


class CaseMissing:
    @parametrize(value=["endpoint", "group_claim"])
    def case_missing(self, value: str) -> str:
        return value


def test_default_attr() -> None:
    d = {"endpoint": random_lower_string(), "group_claim": random_lower_string()}
    item = IdentityProvider(**d)
    assert item.uid is not None
    assert item.description == ""
    assert item.endpoint == d.get("endpoint")
    assert item.group_claim == d.get("group_claim")
    assert isinstance(item.providers, RelationshipManager)
    assert isinstance(item.user_groups, RelationshipManager)


@parametrize_with_cases("missing_attr", cases=CaseMissing)
def test_missing_attr(missing_attr: str) -> None:
    d = {
        "endpoint": None if missing_attr == "endpoint" else random_lower_string(),
        "group_claim": None if missing_attr == "group_claim" else random_lower_string(),
    }
    item = IdentityProvider(**d)
    with pytest.raises(RequiredProperty):
        item.save()
