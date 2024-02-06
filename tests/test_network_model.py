from uuid import uuid4

import pytest
from neomodel import RelationshipManager, RequiredProperty
from pytest_cases import parametrize, parametrize_with_cases

from app.network.models import Network
from tests.common.utils import random_lower_string


class CaseMissing:
    @parametrize(value=["name", "uuid"])
    def case_missing(self, value: str) -> str:
        return value


def test_default_attr() -> None:
    d = {"name": random_lower_string(), "uuid": uuid4().hex}
    item = Network(**d)
    assert item.uid is not None
    assert item.description == ""
    assert item.name == d.get("name")
    assert item.uuid == d.get("uuid")
    assert item.is_shared is False
    assert item.is_router_external is False
    assert item.is_default is False
    assert item.mtu is None
    assert item.proxy_ip is None
    assert item.proxy_user is None
    assert item.tags is None
    assert isinstance(item.project, RelationshipManager)
    assert isinstance(item.service, RelationshipManager)


@parametrize_with_cases("missing_attr", cases=CaseMissing)
def test_missing_attr(missing_attr: str) -> None:
    d = {
        "name": None if missing_attr == "name" else random_lower_string(),
        "uuid": None if missing_attr == "uuid" else uuid4().hex,
    }
    item = Network(**d)
    with pytest.raises(RequiredProperty):
        item.save()
