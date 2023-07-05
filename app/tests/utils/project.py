from .utils import random_lower_string
from ...project.crud import project
from ...project.models import Project
from ...project.schemas import ProjectCreate, ProjectUpdate


def create_random_project() -> Project:
    description = random_lower_string()
    public_network_name = random_lower_string()
    private_network_name = random_lower_string()
    private_network_proxy_host = random_lower_string()
    private_network_proxy_user = random_lower_string()
    item_in = ProjectCreate(
        description=description,
        public_network_name=public_network_name,
        private_network_name=private_network_name,
        private_network_proxy_host=private_network_proxy_host,
        private_network_proxy_user=private_network_proxy_user,
    )
    return project.create(obj_in=item_in)


def create_random_update_project_data() -> ProjectUpdate:
    description = random_lower_string()
    public_network_name = random_lower_string()
    private_network_name = random_lower_string()
    private_network_proxy_host = random_lower_string()
    private_network_proxy_user = random_lower_string()
    return ProjectUpdate(
        description=description,
        public_network_name=public_network_name,
        private_network_name=private_network_name,
        private_network_proxy_host=private_network_proxy_host,
        private_network_proxy_user=private_network_proxy_user,
    )
