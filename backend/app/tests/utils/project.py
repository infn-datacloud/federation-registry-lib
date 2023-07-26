from uuid import uuid4
from app.project.crud import project
from app.project.models import Project
from app.project.schemas import ProjectCreate, ProjectUpdate
from app.tests.utils.provider import create_random_provider
from app.tests.utils.utils import random_lower_string


def create_random_project() -> Project:
    description = random_lower_string()
    name = random_lower_string()
    uuid = uuid4()
    public_network_name = random_lower_string()
    private_network_name = random_lower_string()
    private_network_proxy_host = random_lower_string()
    private_network_proxy_user = random_lower_string()
    item_in = ProjectCreate(
        description=description,
        name=name,
        uuid=uuid,
        public_network_name=public_network_name,
        private_network_name=private_network_name,
        private_network_proxy_host=private_network_proxy_host,
        private_network_proxy_user=private_network_proxy_user,
    )
    return project.create(obj_in=item_in, provider=create_random_provider())


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
