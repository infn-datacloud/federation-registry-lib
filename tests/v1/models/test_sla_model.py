from typing import Any
from unittest.mock import patch

import pytest
from neomodel import (
    AttemptedCardinalityViolation,
    CardinalityViolation,
    RelationshipManager,
    RequiredProperty,
)
from pytest_cases import parametrize_with_cases

from fedreg.v1.project.models import Project
from fedreg.v1.sla.models import SLA
from fedreg.v1.user_group.models import UserGroup
from tests.v1.models.utils import project_model_dict, user_group_model_dict


@parametrize_with_cases("data", has_tag=("dict", "valid"))
def test_sla_valid_attr(data: dict[str, Any]) -> None:
    """Test attribute values (default and set)."""
    item = SLA(**data)
    assert isinstance(item, SLA)
    assert item.uid is not None
    assert item.description == data.get("description", "")
    assert item.doc_uuid == data.get("doc_uuid")
    assert item.start_date == data.get("start_date")
    assert item.end_date == data.get("end_date")

    saved = item.save()
    assert saved.element_id_property
    assert saved.uid == item.uid


@parametrize_with_cases("data, attr", has_tag=("dict", "invalid"))
def test_missing_mandatory_attr(data: dict[str, Any], attr: str) -> None:
    """Test SLA required attributes.

    Creating a model without required values raises a RequiredProperty error.
    """
    err_msg = f"property '{attr}' on objects of class {SLA.__name__}"
    with pytest.raises(RequiredProperty, match=err_msg):
        SLA(**data).save()


def test_rel_def(sla_model: SLA) -> None:
    """Test relationships definition."""
    assert isinstance(sla_model.user_group, RelationshipManager)
    assert sla_model.user_group.name
    assert sla_model.user_group.source
    assert isinstance(sla_model.user_group.source, SLA)
    assert sla_model.user_group.source.uid == sla_model.uid
    assert sla_model.user_group.definition
    assert sla_model.user_group.definition["node_class"] == UserGroup

    assert isinstance(sla_model.projects, RelationshipManager)
    assert sla_model.projects.name
    assert sla_model.projects.source
    assert isinstance(sla_model.projects.source, SLA)
    assert sla_model.projects.source.uid == sla_model.uid
    assert sla_model.projects.definition
    assert sla_model.projects.definition["node_class"] == Project


def test_required_rel(sla_model: SLA) -> None:
    """Test SLA required relationships.

    A model without required relationships can exist but when querying those values, it
    raises a CardinalityViolation error.
    """
    with pytest.raises(CardinalityViolation):
        sla_model.user_group.all()
    with pytest.raises(CardinalityViolation):
        sla_model.user_group.single()
    with pytest.raises(CardinalityViolation):
        sla_model.projects.all()
    with pytest.raises(CardinalityViolation):
        sla_model.projects.single()


def test_single_linked_user_group(sla_model: SLA, user_group_model: UserGroup) -> None:
    """Verify `user_group` relationship works correctly.

    Connect a single UserGroup to an SLA.
    """
    sla_model.user_group.connect(user_group_model)

    assert len(sla_model.user_group.all()) == 1
    user_group = sla_model.user_group.single()
    assert isinstance(user_group, UserGroup)
    assert user_group.uid == user_group_model.uid


def test_multiple_linked_user_group(sla_model: SLA) -> None:
    """Verify `user_group` relationship works correctly.

    Trying to connect multiple UserGroup to an SLA raises an
    AttemptCardinalityViolation error.
    """
    item = UserGroup(**user_group_model_dict()).save()
    sla_model.user_group.connect(item)
    item = UserGroup(**user_group_model_dict()).save()
    with pytest.raises(AttemptedCardinalityViolation):
        sla_model.user_group.connect(item)

    with patch("neomodel.sync_.match.QueryBuilder._count", return_value=0):
        sla_model.user_group.connect(item)
        with pytest.raises(CardinalityViolation):
            sla_model.user_group.all()


def test_single_linked_project(sla_model: SLA, project_model: Project) -> None:
    """Verify `project` relationship works correctly.

    Connect a single Project to an SLA.
    """
    sla_model.projects.connect(project_model)

    assert len(sla_model.projects.all()) == 1
    project = sla_model.projects.single()
    assert isinstance(project, Project)
    assert project.uid == project_model.uid


def test_multiple_linked_projects(sla_model: SLA) -> None:
    """Verify `projects` relationship works correctly.

    Connect multiple Project to an SLA.
    """
    item = Project(**project_model_dict()).save()
    sla_model.projects.connect(item)
    item = Project(**project_model_dict()).save()
    sla_model.projects.connect(item)
    assert len(sla_model.projects.all()) == 2
