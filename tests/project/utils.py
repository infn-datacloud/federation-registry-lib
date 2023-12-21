"""Project utilities."""

from typing import Any, Dict, Union
from uuid import uuid4

from app.project.models import Project
from app.project.schemas import (
    ProjectBase,
    ProjectBasePublic,
    ProjectRead,
    ProjectReadPublic,
)
from app.project.schemas_extended import ProjectReadExtended, ProjectReadExtendedPublic
from tests.common.schemas.validators import ReadSchemaValidation
from tests.common.utils import random_lower_string


class ReadProjectValidation(
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
    """Custom class to validate Read Schemas for Project."""

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
        """Custom function to validate read attributes.

        Exclude form the validation with the DB isntance the 'private_flavors',
        'private_images' and 'private_networks' attributes.
        """
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


def random_project_required_attr() -> Dict[str, Any]:
    """Return a dict with the Project required attributes initialized."""
    return {"name": random_lower_string(), "uuid": uuid4()}


def random_project_all_attr() -> Dict[str, Any]:
    """Dict with all Project attributes."""
    return {**random_project_required_attr(), "description": random_lower_string()}
