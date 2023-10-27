import pytest
from app.project.models import Project
from app.project.schemas import ProjectRead, ProjectReadPublic, ProjectReadShort
from app.project.schemas_extended import ProjectReadExtended, ProjectReadExtendedPublic
from pydantic import ValidationError
from tests.utils.project import (
    create_random_project,
    validate_read_extended_project_attrs,
    validate_read_extended_public_project_attrs,
    validate_read_project_attrs,
    validate_read_public_project_attrs,
    validate_read_short_project_attrs,
)


def test_create_schema():
    """Create a valid 'Create' Schema."""
    create_random_project()
    create_random_project(default=True)


def test_invalid_create_schema():
    """List all invalid situations for a 'Create' Schema."""
    a = create_random_project()
    with pytest.raises(ValidationError):
        a.uuid = None
    with pytest.raises(ValidationError):
        a.name = None


def test_read_schema(db_project: Project):
    """Create a valid 'Read' Schema from DB object.

    Apply conversion for this item for all read schemas. No one of them
    should raise errors.

    Target project has no relationships except for provider.
    """
    schema = ProjectRead.from_orm(db_project)
    validate_read_project_attrs(obj_out=schema, db_item=db_project)
    schema = ProjectReadShort.from_orm(db_project)
    validate_read_short_project_attrs(obj_out=schema, db_item=db_project)
    schema = ProjectReadPublic.from_orm(db_project)
    validate_read_public_project_attrs(obj_out=schema, db_item=db_project)
    schema = ProjectReadExtended.from_orm(db_project)
    validate_read_extended_project_attrs(obj_out=schema, db_item=db_project)
    schema = ProjectReadExtendedPublic.from_orm(db_project)
    validate_read_extended_public_project_attrs(obj_out=schema, db_item=db_project)
