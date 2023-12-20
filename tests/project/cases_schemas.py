"""Project specific cases."""
from typing import Any, Dict, Tuple, Type, Union

from pytest_cases import case, parametrize

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
from tests.project.utils import ReadProjectValidation


@case(tags="create_valid")
def case_project_create_valid_schema_actors(
    project_create_valid_data: Dict[str, Any],
) -> Tuple[
    Type[ProjectCreate],
    CreateSchemaValidation[ProjectBase, ProjectBasePublic, ProjectCreate],
    Dict[str, Any],
]:
    """Fixture with the create class, validator and data to validate."""
    validator = CreateSchemaValidation[ProjectBase, ProjectBasePublic, ProjectCreate](
        base=ProjectBase, base_public=ProjectBasePublic, create=ProjectCreate
    )
    return ProjectCreate, validator, project_create_valid_data


@case(tags="create_invalid")
def case_project_create_invalid_schema_actors(
    project_create_invalid_data: Dict[str, Any],
) -> Tuple[Type[ProjectCreate], Dict[str, Any]]:
    """Fixture with the create class and the invalid data to validate."""
    return ProjectCreate, project_create_invalid_data


@case(tags="patch_valid")
def case_project_patch_valid_schema_actors(
    project_patch_valid_data: Dict[str, Any],
) -> Tuple[
    Type[ProjectUpdate],
    PatchSchemaValidation[ProjectBase, ProjectBasePublic],
    Dict[str, Any],
]:
    """Fixture with the update class, validator and data to validate."""
    validator = PatchSchemaValidation[ProjectBase, ProjectBasePublic](
        base=ProjectBase, base_public=ProjectBasePublic
    )
    return ProjectUpdate, validator, project_patch_valid_data


@case(tags="patch_invalid")
def case_project_patch_invalid_schema_actors(
    project_patch_invalid_data: Dict[str, Any],
) -> Tuple[Type[ProjectUpdate], Dict[str, Any]]:
    """Fixture with the update class and the invalid data to validate."""
    return ProjectUpdate, project_patch_invalid_data


@case(tags="read")
@parametrize(
    cls=[ProjectRead, ProjectReadExtended, ProjectReadPublic, ProjectReadExtendedPublic]
)
def case_project_valid_read_schema_tuple(
    cls: Union[
        ProjectRead, ProjectReadExtended, ProjectReadPublic, ProjectReadExtendedPublic
    ],
    db_project: Project,
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
    bool,
    bool,
]:
    """Fixture with the read class, validator and the db item to read."""
    validator = ReadProjectValidation(
        base=ProjectBase,
        base_public=ProjectBasePublic,
        read=ProjectRead,
        read_extended=ProjectReadExtended,
    )
    cls_name = cls.__name__
    is_public = False
    is_extended = False
    if "Public" in cls_name:
        is_public = True
    if "Extended" in cls_name:
        is_extended = True
    return cls, validator, db_project, is_public, is_extended
