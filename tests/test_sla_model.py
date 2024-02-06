from uuid import uuid4

import pytest
from neomodel import RelationshipManager, RequiredProperty
from pytest_cases import parametrize, parametrize_with_cases

from app.sla.models import SLA
from tests.common.utils import random_date


class CaseMissing:
    @parametrize(value=["doc_uuid", "start_date", "end_date"])
    def case_missing(self, value: str) -> str:
        return value


def test_default_attr() -> None:
    d = {
        "doc_uuid": uuid4().hex,
        "start_date": random_date(),
        "end_date": random_date(),
    }
    item = SLA(**d)
    assert item.uid is not None
    assert item.description == ""
    assert item.doc_uuid == d.get("doc_uuid")
    assert item.start_date == d.get("start_date")
    assert item.end_date == d.get("end_date")
    assert isinstance(item.user_group, RelationshipManager)
    assert isinstance(item.projects, RelationshipManager)


@parametrize_with_cases("missing_attr", cases=CaseMissing)
def test_missing_attr(missing_attr: str) -> None:
    d = {
        "doc_uuid": None if missing_attr == "doc_uuid" else uuid4().hex,
        "start_date": None if missing_attr == "start_date" else random_date(),
        "end_date": None if missing_attr == "end_date" else random_date(),
    }
    item = SLA(**d)
    with pytest.raises(RequiredProperty):
        item.save()
