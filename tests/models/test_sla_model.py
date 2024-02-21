from typing import Any, Tuple
from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from neo4j.graph import Node
from neomodel import CardinalityViolation, RelationshipManager, RequiredProperty
from pytest_cases import parametrize, parametrize_with_cases

from fed_reg.sla.models import SLA
from tests.create_dict import sla_dict
from tests.utils import random_lower_string


class CaseMissing:
    @parametrize(value=["doc_uuid", "start_date", "end_date"])
    def case_missing(self, value: str) -> str:
        return value


class CaseAttr:
    @parametrize(key=["description"])
    def case_str(self, key: str) -> Tuple[str, str]:
        return key, random_lower_string()


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


@parametrize_with_cases("key, value", cases=CaseAttr)
def test_attr(db_core: MagicMock, key: str, value: Any) -> None:
    d = sla_dict()
    d[key] = value

    element_id = f"{db_core.database_version}:{uuid4().hex}:0"
    db_core.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=0, properties=d)]],
        None,
    )

    item = SLA(**d)
    saved = item.save()

    assert saved.element_id_property == element_id
    assert saved.uid == item.uid
    assert saved.__getattribute__(key) == value


def test_required_rel(db_match: MagicMock, sla_model: SLA) -> None:
    db_match.cypher_query.return_value = ([], None)
    with pytest.raises(CardinalityViolation):
        sla_model.user_group.all()
    with pytest.raises(CardinalityViolation):
        sla_model.user_group.single()
    with pytest.raises(CardinalityViolation):
        sla_model.projects.all()
    with pytest.raises(CardinalityViolation):
        sla_model.projects.single()
