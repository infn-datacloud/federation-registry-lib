from typing import Any, Dict, Tuple
from unittest.mock import Mock, PropertyMock, patch
from uuid import uuid4

import pytest
from neo4j.graph import Node
from neomodel import RelationshipManager, RequiredProperty
from pytest_cases import parametrize, parametrize_with_cases

from app.sla.models import SLA
from tests.common.utils import random_date, random_lower_string


class CaseMissing:
    @parametrize(value=["doc_uuid", "start_date", "end_date"])
    def case_missing(self, value: str) -> str:
        return value


class CaseAttr:
    @parametrize(key=["description"])
    def case_str(self, key: str) -> Tuple[str, str]:
        return key, random_lower_string()


def sla_dict() -> Dict[str, Any]:
    return {
        "doc_uuid": uuid4().hex,
        "start_date": random_date(),
        "end_date": random_date(),
    }


def test_default_attr() -> None:
    d = sla_dict()
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
    d = sla_dict()
    d[missing_attr] = None
    item = SLA(**d)
    with pytest.raises(RequiredProperty):
        item.save()


@patch("neomodel.core.db")
@parametrize_with_cases("key, value", cases=CaseAttr)
def test_attr(mock_db: Mock, key: str, value: Any) -> None:
    d = sla_dict()
    d[key] = value

    db_version = "5"
    type(mock_db).database_version = PropertyMock(return_value=db_version)
    element_id = f"{db_version}:{uuid4().hex}:0"
    mock_db.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=0, properties=d)]],
        None,
    )

    item = SLA(**d)
    saved = item.save()

    assert saved.element_id_property == element_id
    assert saved.uid == item.uid
    assert saved.__getattribute__(key) == value
