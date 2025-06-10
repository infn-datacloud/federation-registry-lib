from typing import Any, Literal

from pytest_cases import case, parametrize_with_cases

from fedreg.v1.project.models import Project
from fedreg.v1.project.schemas import ProjectBase, ProjectCreate
from tests.v1.schemas.utils import project_schema_dict
from tests.v1.utils import random_lower_string


class CaseProjectSchema:
    @case(tags=("dict", "valid", "base_public", "base", "update"))
    def case_mandatory(self) -> dict[str, Any]:
        return project_schema_dict()

    @case(tags=("dict", "valid", "base_public", "base", "update"))
    def case_description(self) -> dict[str, Any]:
        return {**project_schema_dict(), "description": random_lower_string()}

    @case(tags=("dict", "invalid", "base_public", "base", "read_public", "read"))
    def case_missing_name(self) -> tuple[dict[str, Any], Literal["name"]]:
        d = project_schema_dict()
        d.pop("name")
        return d, "name"

    @case(tags=("dict", "invalid", "base_public", "base", "read_public", "read"))
    def case_missing_uuid(self) -> tuple[dict[str, Any], Literal["uuid"]]:
        d = project_schema_dict()
        d.pop("uuid")
        return d, "uuid"

    @case(tags="class")
    def case_base_class(self) -> type[ProjectBase]:
        return ProjectBase

    @case(tags="class")
    def case_create_class(self) -> type[ProjectCreate]:
        return ProjectCreate


class CaseModel:
    @case(tags="model")
    @parametrize_with_cases(
        "data", cases=CaseProjectSchema, has_tag=("dict", "valid", "base")
    )
    def case_project_model(self, data: dict[str, Any]) -> Project:
        return Project(**ProjectCreate(**data).dict()).save()
