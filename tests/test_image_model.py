from uuid import uuid4

import pytest
from neomodel import RelationshipManager, RequiredProperty
from pytest_cases import parametrize, parametrize_with_cases

from app.image.models import Image
from tests.common.utils import random_lower_string


class CaseMissing:
    @parametrize(value=["name", "uuid"])
    def case_missing(self, value: str) -> str:
        return value


def test_default_attr() -> None:
    d = {"name": random_lower_string(), "uuid": uuid4().hex}
    item = Image(**d)
    assert item.uid is not None
    assert item.description == ""
    assert item.name == d.get("name")
    assert item.uuid == d.get("uuid")
    assert item.is_public is True
    assert item.os_type is None
    assert item.os_distro is None
    assert item.os_version is None
    assert item.architecture is None
    assert item.kernel_id is None
    assert item.cuda_support is False
    assert item.gpu_driver is False
    assert item.tags is None
    assert isinstance(item.projects, RelationshipManager)
    assert isinstance(item.services, RelationshipManager)


@parametrize_with_cases("missing_attr", cases=CaseMissing)
def test_missing_attr(missing_attr: str) -> None:
    d = {
        "name": None if missing_attr == "name" else random_lower_string(),
        "uuid": None if missing_attr == "uuid" else uuid4().hex,
    }
    item = Image(**d)
    with pytest.raises(RequiredProperty):
        item.save()
