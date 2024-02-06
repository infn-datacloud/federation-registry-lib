import pytest
from neomodel import RelationshipManager, RequiredProperty
from pytest_cases import parametrize, parametrize_with_cases

from app.location.models import Location
from tests.common.utils import random_lower_string


class CaseMissing:
    @parametrize(value=["site", "country"])
    def case_missing(self, value: str) -> str:
        return value


def test_default_attr() -> None:
    d = {"site": random_lower_string(), "country": random_lower_string()}
    item = Location(**d)
    assert item.uid is not None
    assert item.description == ""
    assert item.site == d.get("site")
    assert item.country == d.get("country")
    assert item.latitude is None
    assert item.longitude is None
    assert isinstance(item.regions, RelationshipManager)


@parametrize_with_cases("missing_attr", cases=CaseMissing)
def test_missing_attr(missing_attr: str) -> None:
    d = {
        "site": None if missing_attr == "site" else random_lower_string(),
        "country": None if missing_attr == "country" else random_lower_string(),
    }
    item = Location(**d)
    with pytest.raises(RequiredProperty):
        item.save()
