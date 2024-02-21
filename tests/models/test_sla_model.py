from typing import Any, Tuple
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest
from neo4j.graph import Node
from neomodel import (
    AttemptedCardinalityViolation,
    CardinalityViolation,
    RelationshipManager,
    RequiredProperty,
)
from pytest_cases import parametrize, parametrize_with_cases

from fed_reg.project.models import Project
from fed_reg.sla.models import SLA
from fed_reg.user_group.models import UserGroup
from tests.create_dict import sla_model_dict
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
    d = sla_model_dict()
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
    d = sla_model_dict()
    d[missing_attr] = None
    item = SLA(**d)
    with pytest.raises(RequiredProperty):
        item.save()


@parametrize_with_cases("key, value", cases=CaseAttr)
def test_attr(db_core: MagicMock, key: str, value: Any) -> None:
    d = sla_model_dict()
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


@patch("neomodel.match.QueryBuilder._count", return_value=0)
def test_linked_user_group(
    mock_count: MagicMock,
    db_rel_mgr: MagicMock,
    db_match: MagicMock,
    sla_model: SLA,
    user_group_model: UserGroup,
) -> None:
    assert sla_model.user_group.name
    assert sla_model.user_group.source
    assert isinstance(sla_model.user_group.source, SLA)
    assert sla_model.user_group.source.uid == sla_model.uid
    assert sla_model.user_group.definition
    assert sla_model.user_group.definition["node_class"] == UserGroup

    r = sla_model.user_group.connect(user_group_model)
    assert r is True

    db_match.cypher_query.return_value = ([[user_group_model]], ["user_group_r1"])
    assert len(sla_model.user_group.all()) == 1
    user_group = sla_model.user_group.single()
    assert isinstance(user_group, UserGroup)
    assert user_group.uid == user_group_model.uid


def test_multiple_linked_user_group(
    db_rel_mgr: MagicMock,
    db_match: MagicMock,
    sla_model: SLA,
    user_group_model: UserGroup,
) -> None:
    with patch("neomodel.match.QueryBuilder._count") as mock_count:
        mock_count.return_value = 1
        with pytest.raises(AttemptedCardinalityViolation):
            sla_model.user_group.connect(user_group_model)

    db_match.cypher_query.return_value = (
        [[user_group_model], [user_group_model]],
        ["user_group_r1", "user_group_r2"],
    )
    with pytest.raises(CardinalityViolation):
        sla_model.user_group.all()


def test_linked_project(
    db_rel_mgr: MagicMock,
    db_match: MagicMock,
    sla_model: SLA,
    project_model: Project,
) -> None:
    assert sla_model.projects.name
    assert sla_model.projects.source
    assert isinstance(sla_model.projects.source, SLA)
    assert sla_model.projects.source.uid == sla_model.uid
    assert sla_model.projects.definition
    assert sla_model.projects.definition["node_class"] == Project

    r = sla_model.projects.connect(project_model)
    assert r is True

    db_match.cypher_query.return_value = ([[project_model]], ["projects_r1"])
    assert len(sla_model.projects.all()) == 1
    project = sla_model.projects.single()
    assert isinstance(project, Project)
    assert project.uid == project_model.uid


def test_multiple_linked_projects(
    db_rel_mgr: MagicMock,
    db_match: MagicMock,
    sla_model: SLA,
    project_model: Project,
) -> None:
    db_match.cypher_query.return_value = (
        [[project_model], [project_model]],
        ["projects_r1", "projects_r2"],
    )
    assert len(sla_model.projects.all()) == 2
