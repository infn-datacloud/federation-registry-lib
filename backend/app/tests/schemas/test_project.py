import pytest
from app.project.crud import project
from app.project.schemas import ProjectRead, ProjectReadPublic, ProjectReadShort
from app.project.schemas_extended import ProjectReadExtended, ProjectReadExtendedPublic
from app.provider.models import Provider
from app.tests.utils.project import create_random_project
from pydantic import ValidationError


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


def test_read_schema(db_provider: Provider):
    """Create a valid 'Read' Schema."""
    obj_in = create_random_project()
    db_obj = project.create(obj_in=obj_in, provider=db_provider)
    ProjectRead.from_orm(db_obj)
    ProjectReadPublic.from_orm(db_obj)
    ProjectReadShort.from_orm(db_obj)
    ProjectReadExtended.from_orm(db_obj)
    ProjectReadExtendedPublic.from_orm(db_obj)

    obj_in = create_random_project(default=True)
    db_obj = project.create(obj_in=obj_in, provider=db_provider)
    ProjectRead.from_orm(db_obj)
    ProjectReadPublic.from_orm(db_obj)
    ProjectReadShort.from_orm(db_obj)
    ProjectReadExtended.from_orm(db_obj)
    ProjectReadExtendedPublic.from_orm(db_obj)
