from uuid import uuid4

from app.project.models import Project
from app.project.schemas import ProjectCreate, ProjectUpdate
from app.tests.utils.utils import random_lower_string


def create_random_project(default: bool = False) -> ProjectCreate:
    name = random_lower_string()
    uuid = uuid4()
    kwargs = {}
    if not default:
        kwargs = {"description": random_lower_string()}
    return ProjectCreate(name=name, uuid=uuid, **kwargs)


def create_random_project_patch(default: bool = False) -> ProjectUpdate:
    if default:
        return ProjectUpdate()
    description = random_lower_string()
    name = random_lower_string()
    uuid = uuid4()
    return ProjectUpdate(description=description, name=name, uuid=uuid)


def validate_project_attrs(
    *, obj_in: ProjectCreate, db_item: Project
) -> None:
    assert db_item.description == obj_in.description
    assert db_item.name == obj_in.name
    assert db_item.uuid == obj_in.uuid
