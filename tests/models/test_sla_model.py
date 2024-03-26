from typing import Any, Tuple
from unittest.mock import patch

import pytest
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
from tests.create_dict import project_model_dict, sla_model_dict, user_group_model_dict
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
def test_attr(key: str, value: Any) -> None:
    d = sla_model_dict()
    d[key] = value

    item = SLA(**d)
    saved = item.save()

    assert saved.element_id_property
    assert saved.uid == item.uid
    assert saved.__getattribute__(key) == value


def test_required_rel(sla_model: SLA) -> None:
    with pytest.raises(CardinalityViolation):
        sla_model.user_group.all()
    with pytest.raises(CardinalityViolation):
        sla_model.user_group.single()
    with pytest.raises(CardinalityViolation):
        sla_model.projects.all()
    with pytest.raises(CardinalityViolation):
        sla_model.projects.single()


def test_linked_user_group(sla_model: SLA, user_group_model: UserGroup) -> None:
    assert sla_model.user_group.name
    assert sla_model.user_group.source
    assert isinstance(sla_model.user_group.source, SLA)
    assert sla_model.user_group.source.uid == sla_model.uid
    assert sla_model.user_group.definition
    assert sla_model.user_group.definition["node_class"] == UserGroup

    r = sla_model.user_group.connect(user_group_model)
    assert r is True

    assert len(sla_model.user_group.all()) == 1
    user_group = sla_model.user_group.single()
    assert isinstance(user_group, UserGroup)
    assert user_group.uid == user_group_model.uid


def test_multiple_linked_user_group(sla_model: SLA) -> None:
    item = UserGroup(**user_group_model_dict()).save()
    sla_model.user_group.connect(item)
    item = UserGroup(**user_group_model_dict()).save()
    with pytest.raises(AttemptedCardinalityViolation):
        sla_model.user_group.connect(item)

    with patch("neomodel.match.QueryBuilder._count", return_value=0):
        sla_model.user_group.connect(item)
        with pytest.raises(CardinalityViolation):
            sla_model.user_group.all()


def test_linked_project(sla_model: SLA, project_model: Project) -> None:
    assert sla_model.projects.name
    assert sla_model.projects.source
    assert isinstance(sla_model.projects.source, SLA)
    assert sla_model.projects.source.uid == sla_model.uid
    assert sla_model.projects.definition
    assert sla_model.projects.definition["node_class"] == Project

    r = sla_model.projects.connect(project_model)
    assert r is True

    assert len(sla_model.projects.all()) == 1
    project = sla_model.projects.single()
    assert isinstance(project, Project)
    assert project.uid == project_model.uid


def test_multiple_linked_projects(sla_model: SLA) -> None:
    item = Project(**project_model_dict()).save()
    sla_model.projects.connect(item)
    item = Project(**project_model_dict()).save()
    sla_model.projects.connect(item)
    assert len(sla_model.projects.all()) == 2
