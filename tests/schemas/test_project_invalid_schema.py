from typing import Any

import pytest
from pytest_cases import parametrize_with_cases

from fed_reg.project.models import Project
from fed_reg.project.schemas import (
    ProjectBase,
    ProjectBasePublic,
    ProjectRead,
    ProjectReadPublic,
)
from tests.create_dict import project_schema_dict


@parametrize_with_cases("key, value")
def test_invalid_base_public(key: str, value: None) -> None:
    d = project_schema_dict()
    d[key] = value
    with pytest.raises(ValueError):
        ProjectBasePublic(**d)


@parametrize_with_cases("key, value")
def test_invalid_base(key: str, value: Any) -> None:
    d = project_schema_dict()
    d[key] = value
    with pytest.raises(ValueError):
        ProjectBase(**d)


@parametrize_with_cases("key, value")
def test_invalid_read_public(project_model: Project, key: str, value: str) -> None:
    project_model.__setattr__(key, value)
    with pytest.raises(ValueError):
        ProjectReadPublic.from_orm(project_model)


@parametrize_with_cases("key, value")
def test_invalid_read(project_model: Project, key: str, value: str) -> None:
    project_model.__setattr__(key, value)
    with pytest.raises(ValueError):
        ProjectRead.from_orm(project_model)
