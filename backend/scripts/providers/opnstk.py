from typing import Any, Dict, List

from logger import logger
from models.cmdb import (
    FlavorWrite,
    ImageWrite,
    ProjectWrite,
    ProviderWrite,
    ServiceWrite,
)
from models.config import IDP, Openstack
from openstack import connect
from openstack.connection import Connection
from utils import get_identity_providers


def get_project(conn: Connection) -> ProjectWrite:
    logger.info("Retrieve current project data")
    curr_proj_id = conn.current_project.get("id")
    project = conn.identity.get_project(curr_proj_id)
    data = project.to_dict()
    data["uuid"] = data.pop("id")
    if data.get("description") is None:
        data["description"] = ""
    return ProjectWrite(**data)


def get_flavors(conn: Connection) -> List[FlavorWrite]:
    logger.info("Retrieve current project accessible flavors")
    flavors = []
    for flavor in conn.compute.flavors():
        projects = []
        if not flavor.is_public:
            projects = conn.compute.get_flavor_access(flavor)
        data = flavor.to_dict()
        data["uuid"] = data.pop("id")
        if data.get("description") is None:
            data["description"] = ""
        flavors.append(FlavorWrite(**data, projects=projects))
    return flavors


def get_images(conn: Connection) -> List[ImageWrite]:
    logger.info("Retrieve current project accessible images")
    images = []
    for image in conn.image.images():
        is_public = True
        projects = []
        if image.visibility in ["private", "shared"]:
            projects = [image.owner_id]
            is_public = False
        if image.visibility == "shared":
            members = list(conn.image.members(image))
            for member in members:
                if member.status == "accepted":
                    projects.append(member.id)
        data = image.to_dict()
        data["uuid"] = data.pop("id")
        if data.get("description") is None:
            data["description"] = ""
        data["version"] = data.pop("os_version")
        data["distribution"] = data.pop("os_distro")
        data["is_public"] = is_public
        data.pop("visibility")
        images.append(ImageWrite(**data, projects=projects))
    return images


def get_quotas(conn: Connection) -> Dict[str, Any]:
    logger.info("Retrieve current project accessible quotas")
    quota_set = {}
    for k, v in conn.compute.get_quota_set(conn.current_project_id).items():
        quota_set[conn.compute.service_type] = {}
        if k not in ["project_id", "id", "name"]:
            quota_set[conn.compute.service_type][k] = v
    for k, v in conn.block_storage.get_quota_set(conn.current_project_id).items():
        quota_set[conn.block_storage.service_type] = {}
        if k not in ["project_id", "id", "name"]:
            quota_set[conn.compute.service_type][k] = v
    return quota_set


def get_services(conn: Connection) -> List[ServiceWrite]:
    return [
        ServiceWrite(
            endpoint=conn.auth.get("auth_url"),
            type=conn.identity.service_type,
            name="org.openstack.keystone",
        ),
        ServiceWrite(
            endpoint=conn.compute.get_endpoint(),
            type=conn.compute.service_type,
            name="org.openstack.nova",
        ),
        ServiceWrite(
            endpoint=conn.block_storage.get_endpoint(),
            type=conn.block_storage.service_type,
            name="org.openstack.cinder",
        ),
    ]


#         if not quota.is_public:
# projects = conn.compute.get_quota_access(quota)
# data = quota.to_dict()
# data["uuid"] = data.pop("id")
# if data.get("description") is None:
# data["description"] = ""
# quotas.append(FlavorWrite(**data, projects=projects))
# return quotas


def get_os_provider(*, config: Openstack, chosen_idp: IDP, token: str) -> ProviderWrite:
    """Generate an Openstack virtual provider, reading information from a real
    openstack instance."""
    provider = ProviderWrite(
        name=config.name,
        is_public=config.is_public,
        support_emails=config.support_emails,
        location=config.location,
        identity_providers=get_identity_providers(config.identity_providers),
    )

    for project in config.projects:
        if project.id is not None:
            logger.info(
                f"Connecting to openstack instance with project ID: {project.id}"
            )
        else:
            logger.info(
                "Connecting to openstack instance with project"
                f"name and domain: {project.name} - {project.domain}"
            )
        conn = connect(
            auth_url=config.auth_url,
            auth_type="v3oidcaccesstoken",
            identity_provider=chosen_idp.name,
            protocol=chosen_idp.protocol,
            access_token=token,
            project_id=project.id,
            project_name=project.name,
            project_domain_name=project.domain,
        )

        if len(provider.services) == 0:
            provider.services = get_services(conn)

        provider.projects.append(get_project(conn))

        flavors = get_flavors(conn)
        uids = [j.uuid for j in provider.flavors]
        for i in flavors:
            if i.uuid not in uids:
                provider.flavors.append(i)

        images = get_images(conn)
        uids = [j.uuid for j in provider.images]
        for i in images:
            if i.uuid not in uids:
                provider.images.append(i)

        provider.quotas[conn.current_project_id] = get_quotas(conn)

        conn.close()
        logger.info("Connection closed")

    return provider
