from typing import List

from logger import logger
from models.cmdb.flavor import FlavorWrite
from models.cmdb.image import ImageWrite
from models.cmdb.project import ProjectWrite
from models.cmdb.provider import ProviderWrite
from models.cmdb.quota import BlockStorageQuotaWrite, ComputeQuotaWrite
from models.cmdb.service import ServiceWrite
from models.cmdb.sla import SLAWrite
from models.cmdb.user_group import UserGroupWrite
from models.config import IDP, Openstack
from openstack import connect
from openstack.connection import Connection
from utils import get_identity_providers, get_per_user_quotas


def get_block_storage_quotas(conn: Connection) -> BlockStorageQuotaWrite:
    logger.info("Retrieve current project accessible block storage quotas")
    quota = conn.block_storage.get_quota_set(conn.current_project_id)
    data = quota.to_dict()
    return BlockStorageQuotaWrite(**data, service=conn.block_storage.get_endpoint())


def get_compute_quotas(conn: Connection) -> ComputeQuotaWrite:
    logger.info("Retrieve current project accessible compute quotas")
    quota = conn.compute.get_quota_set(conn.current_project_id)
    data = quota.to_dict()
    return ComputeQuotaWrite(**data, service=conn.compute.get_endpoint())


def get_flavors(conn: Connection) -> List[FlavorWrite]:
    logger.info("Retrieve current project accessible flavors")
    flavors = []
    for flavor in conn.compute.flavors():
        projects = []
        if not flavor.is_public:
            for i in conn.compute.get_flavor_access(flavor):
                projects.append(i.get("tenant_id"))
        data = flavor.to_dict()
        data["uuid"] = data.pop("id")
        if data.get("description") is None:
            data["description"] = ""
        extra = data.pop("extra_specs")
        if extra:
            data["gpus"] = extra.get("gpu_number", 0)
            data["gpu_model"] = extra.get("gpu_model")
            data["gpu_vendor"] = extra.get("gpu_vendor")
            data["local_storage"] = extra.get(
                "aggregate_instance_extra_specs:local_storage"
            )
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


def get_project(conn: Connection) -> ProjectWrite:
    logger.info("Retrieve current project data")
    curr_proj_id = conn.current_project.get("id")
    project = conn.identity.get_project(curr_proj_id)
    data = project.to_dict()
    data["uuid"] = data.pop("id")
    if data.get("description") is None:
        data["description"] = ""
    return ProjectWrite(**data)


def get_services(conn: Connection) -> List[ServiceWrite]:
    logger.info("Retrieve current region accessible services")
    return [
        ServiceWrite(
            endpoint=conn.auth.get("auth_url"),
            type=conn.identity.service_type,
            name="org.openstack.keystone",
            region=conn.identity.region_name,
        ),
        ServiceWrite(
            endpoint=conn.compute.get_endpoint(),
            type=conn.compute.service_type,
            name="org.openstack.nova",
            region=conn.compute.region_name,
        ),
        ServiceWrite(
            endpoint=conn.block_storage.get_endpoint(),
            type=conn.block_storage.service_type,
            name="org.openstack.cinder",
            region=conn.block_storage.region_name,
        ),
    ]


def get_provider(*, config: Openstack, chosen_idp: IDP, token: str) -> ProviderWrite:
    """Generate an Openstack virtual provider, reading information from a real
    openstack instance."""
    provider = ProviderWrite(
        name=config.name,
        is_public=config.is_public,
        support_emails=config.support_emails,
        location=config.location,
        status=config.status,
        identity_providers=get_identity_providers(config.identity_providers),
    )

    for sla in config.slas:
        project = sla.project
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

        proj = get_project(conn)
        compute_quota = get_compute_quotas(conn)
        block_storage_quota = get_block_storage_quotas(conn)
        per_user_comp_quota, per_user_blk_sto_quota = get_per_user_quotas(
            per_user_limits=project.per_user_limits,
            compute_service=compute_quota.service,
            block_storage_service=block_storage_quota.service,
        )
        proj.quotas.append(compute_quota)
        proj.quotas.append(block_storage_quota)
        if per_user_comp_quota is not None:
            proj.quotas.append(per_user_comp_quota)
        if per_user_blk_sto_quota is not None:
            proj.quotas.append(per_user_blk_sto_quota)
        user_group = UserGroupWrite(
            name=project.group.name, identity_provider=project.group.idp
        )
        proj.sla = SLAWrite(**sla.dict(), user_group=user_group)
        provider.projects.append(proj)

        flavors = get_flavors(conn)
        uuids = [j.uuid for j in provider.flavors]
        for i in flavors:
            if i.uuid not in uuids:
                provider.flavors.append(i)

        images = get_images(conn)
        uuids = [j.uuid for j in provider.images]
        for i in images:
            if i.uuid not in uuids:
                provider.images.append(i)

        services = get_services(conn)
        endpoints = [j.endpoint for j in provider.services]
        for i in services:
            if i.endpoint not in endpoints:
                provider.services.append(i)

        conn.close()
        logger.info("Connection closed")

    return provider
