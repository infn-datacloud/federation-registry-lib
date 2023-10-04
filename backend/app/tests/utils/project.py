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


def create_random_update_project_data() -> ProjectUpdate:
    description = random_lower_string()
    name = random_lower_string()
    uuid = uuid4()
    public_network_name = random_lower_string()
    private_network_name = random_lower_string()
    private_network_proxy_host = random_lower_string()
    private_network_proxy_user = random_lower_string()
    return ProjectUpdate(
        description=description,
        name=name,
        uuid=uuid,
        public_network_name=public_network_name,
        private_network_name=private_network_name,
        private_network_proxy_host=private_network_proxy_host,
        private_network_proxy_user=private_network_proxy_user,
    )


def validate_project_attrs(*, obj_in: ProjectCreate, db_item: Project) -> None:
    assert db_item.description == obj_in.description
    assert db_item.name == obj_in.name
    assert db_item.uuid == str(obj_in.uuid)
