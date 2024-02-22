from typing import Any, Literal, Tuple

import pytest
from pytest_cases import case, parametrize, parametrize_with_cases

from fed_reg.models import BaseNode, BaseNodeCreate, BaseNodeQuery
from fed_reg.project.schemas import (
    ProjectBase,
    ProjectBasePublic,
    ProjectCreate,
    ProjectQuery,
    ProjectUpdate,
)
from tests.create_dict import project_schema_dict
from tests.utils import random_lower_string


class CaseAttr:
    @case(tags=["base_public", "update"])
    def case_none(self) -> Tuple[None, None]:
        return None, None

    @case(tags=["base_public"])
    def case_desc(self) -> Tuple[Literal["description"], str]:
        return "description", random_lower_string()


class CaseInvalidAttr:
    @case(tags=["base_public", "update"])
    @parametrize(attr=["name", "uuid"])
    def case_attr(self, attr: str) -> Tuple[str, None]:
        return attr, None


@parametrize_with_cases("key, value", cases=CaseAttr, has_tag=["base_public"])
def test_base_public(key: str, value: str) -> None:
    assert issubclass(ProjectBasePublic, BaseNode)
    d = project_schema_dict()
    if key:
        d[key] = value
    item = ProjectBasePublic(**d)
    assert item.description == d.get("description", "")
    assert item.name == d.get("name")
    assert item.uuid == d.get("uuid").hex


@parametrize_with_cases("key, value", cases=CaseInvalidAttr, has_tag=["base_public"])
def test_invalid_base_public(key: str, value: None) -> None:
    d = project_schema_dict()
    d[key] = value
    with pytest.raises(ValueError):
        ProjectBasePublic(**d)


@parametrize_with_cases("key, value", cases=CaseAttr)
def test_base(key: str, value: Any) -> None:
    assert issubclass(ProjectBase, ProjectBasePublic)
    d = project_schema_dict()
    if key:
        d[key] = value
    item = ProjectBase(**d)
    assert item.name == d.get("name")
    assert item.uuid == d.get("uuid").hex


@parametrize_with_cases("key, value", cases=CaseInvalidAttr)
def test_invalid_base(key: str, value: Any) -> None:
    d = project_schema_dict()
    d[key] = value
    with pytest.raises(ValueError):
        ProjectBase(**d)


def test_create() -> None:
    assert issubclass(ProjectCreate, BaseNodeCreate)
    assert issubclass(ProjectCreate, ProjectBase)


@parametrize_with_cases(
    "key, value", cases=[CaseInvalidAttr, CaseAttr], has_tag=["update"]
)
def test_update(key: str, value: Any) -> None:
    assert issubclass(ProjectUpdate, BaseNodeCreate)
    assert issubclass(ProjectUpdate, ProjectBase)
    d = project_schema_dict()
    if key:
        d[key] = value
    item = ProjectUpdate(**d)
    assert item.name == d.get("name")
    assert item.uuid == (d.get("uuid").hex if d.get("uuid") else None)


def test_query() -> None:
    assert issubclass(ProjectQuery, BaseNodeQuery)


# TODO Test all read classes
