"""Project specific fixtures."""
from typing import Any, Dict, Tuple, Type, Union

from pytest_cases import fixture

from app.project.models import Project
from app.project.schemas import (
    ProjectBase,
    ProjectBasePublic,
    ProjectRead,
    ProjectReadPublic,
    ProjectUpdate,
)
from app.project.schemas_extended import ProjectReadExtended, ProjectReadExtendedPublic
from app.provider.schemas_extended import ProjectCreate
from tests.common.schemas.validators import (
    CreateSchemaValidation,
    PatchSchemaValidation,
    ReadSchemaValidation,
)


@fixture
def project_valid_create_schema_tuple(
    project_create_validator, project_create_valid_data
) -> Tuple[
    Type[ProjectCreate],
    CreateSchemaValidation[ProjectBase, ProjectBasePublic, ProjectCreate],
    Dict[str, Any],
]:
    """Fixture with the create class, validator and data to validate."""
    return ProjectCreate, project_create_validator, project_create_valid_data


@fixture
def project_invalid_create_schema_tuple(
    project_create_invalid_data,
) -> Tuple[Type[ProjectCreate], Dict[str, Any]]:
    """Fixture with the create class and the invalid data to validate."""
    return ProjectCreate, project_create_invalid_data


@fixture
def project_valid_patch_schema_tuple(
    project_patch_validator, project_patch_valid_data
) -> Tuple[
    Type[ProjectUpdate],
    PatchSchemaValidation[ProjectBase, ProjectBasePublic],
    Dict[str, Any],
]:
    """Fixture with the update class, validator and data to validate."""
    return ProjectUpdate, project_patch_validator, project_patch_valid_data


@fixture
def project_invalid_patch_schema_tuple(
    project_patch_invalid_data,
) -> Tuple[Type[ProjectUpdate], Dict[str, Any]]:
    """Fixture with the update class and the invalid data to validate."""
    return ProjectUpdate, project_patch_invalid_data


@fixture
def project_valid_read_schema_tuple(
    project_read_class, project_read_validator, db_project
) -> Tuple[
    Union[
        ProjectRead, ProjectReadPublic, ProjectReadExtended, ProjectReadExtendedPublic
    ],
    ReadSchemaValidation[
        ProjectBase,
        ProjectBasePublic,
        ProjectRead,
        ProjectReadPublic,
        ProjectReadExtended,
        ProjectReadExtendedPublic,
        Project,
    ],
    Project,
]:
    """Fixture with the read class, validator and the db item to read."""
    return project_read_class, project_read_validator, db_project
