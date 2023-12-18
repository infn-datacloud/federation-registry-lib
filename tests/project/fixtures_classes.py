"""Project specific fixtures."""
from typing import Any, Union

from pytest_cases import fixture, parametrize

from app.project.models import Project
from app.project.schemas import (
    ProjectBase,
    ProjectBasePublic,
    ProjectRead,
    ProjectReadPublic,
)
from app.project.schemas_extended import ProjectReadExtended, ProjectReadExtendedPublic
from app.provider.schemas_extended import ProjectCreate
from tests.common.schemas.validators import (
    CreateSchemaValidation,
    PatchSchemaValidation,
    ReadSchemaValidation,
)


@fixture
def project_create_validator() -> (
    CreateSchemaValidation[ProjectBase, ProjectBasePublic, ProjectCreate]
):
    """Instance to validate project create schemas."""
    return CreateSchemaValidation[ProjectBase, ProjectBasePublic, ProjectCreate](
        base=ProjectBase, base_public=ProjectBasePublic, create=ProjectCreate
    )


@fixture
def project_read_validator() -> (
    ReadSchemaValidation[
        ProjectBase,
        ProjectBasePublic,
        ProjectRead,
        ProjectReadPublic,
        ProjectReadExtended,
        ProjectReadExtendedPublic,
        Project,
    ]
):
    """Instance to validate project read schemas."""

    class ReadProjectValidaiton(
        ReadSchemaValidation[
            ProjectBase,
            ProjectBasePublic,
            ProjectRead,
            ProjectReadPublic,
            ProjectReadExtended,
            ProjectReadExtendedPublic,
            Project,
        ]
    ):
        def validate_read_attrs(
            self,
            *,
            db_item: Project,
            schema: Union[
                ProjectRead,
                ProjectReadPublic,
                ProjectReadExtended,
                ProjectReadExtendedPublic,
            ],
            public: bool,
            extended: bool,
        ) -> None:
            return super().validate_read_attrs(
                db_item=db_item,
                schema=schema,
                public=public,
                extended=extended,
                exclude_attrs=[
                    "private_images",
                    "private_flavors",
                    "private_networks",
                ],
            )

    return ReadProjectValidaiton(
        base=ProjectBase,
        base_public=ProjectBasePublic,
        read=ProjectRead,
        read_extended=ProjectReadExtended,
    )


@fixture
def project_patch_validator() -> PatchSchemaValidation[ProjectBase, ProjectBasePublic]:
    """Instance to validate project patch schemas."""
    return PatchSchemaValidation[ProjectBase, ProjectBasePublic](
        base=ProjectBase, base_public=ProjectBasePublic
    )


@fixture
@parametrize(
    cls=[ProjectRead, ProjectReadExtended, ProjectReadPublic, ProjectReadExtendedPublic]
)
def project_read_class(cls) -> Any:
    """Project Read schema."""
    return cls
