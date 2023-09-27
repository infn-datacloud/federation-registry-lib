import copy
import os
from typing import List

from logger import logger
from models.cmdb.flavor import FlavorWrite
from models.cmdb.image import ImageWrite
from models.cmdb.network import NetworkWrite
from models.cmdb.project import ProjectWrite
from models.cmdb.provider import ProviderWrite
from models.cmdb.quota import BlockStorageQuotaWrite, ComputeQuotaWrite
from models.cmdb.region import RegionWrite
from models.cmdb.service import (
    BlockStorageServiceWrite,
    ComputeServiceWrite,
    IdentityServiceWrite,
    NetworkServiceWrite,
)
from models.config import AuthMethod, Openstack, OsProject, TrustedIDPOut
from openstack import connect
from openstack.connection import Connection
from utils import get_per_user_block_storage_quotas, get_per_user_compute_quotas

TIMEOUT = 2  # s


def get_block_storage_quotas(conn: Connection) -> BlockStorageQuotaWrite:
    logger.info("Retrieve current project accessible block storage quotas")
    quota = conn.block_storage.get_quota_set(conn.current_project_id)
    data = quota.to_dict()
    return BlockStorageQuotaWrite(**data, project=conn.current_project_id)


def get_compute_quotas(conn: Connection) -> ComputeQuotaWrite:
    logger.info("Retrieve current project accessible compute quotas")
    quota = conn.compute.get_quota_set(conn.current_project_id)
    data = quota.to_dict()
    return ComputeQuotaWrite(**data, project=conn.current_project_id)


def get_flavors(conn: Connection) -> List[FlavorWrite]:
    logger.info("Retrieve current project accessible flavors")
    flavors = []
    for flavor in conn.compute.flavors(is_disabled=False):
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
            data["gpus"] = int(extra.get("gpu_number", 0))
            data["gpu_model"] = extra.get("gpu_model") if data["gpus"] > 0 else None
            data["gpu_vendor"] = extra.get("gpu_vendor") if data["gpus"] > 0 else None
            data["local_storage"] = extra.get(
                "aggregate_instance_extra_specs:local_storage"
            )
            data["infiniband"] = extra.get("infiniband", False)
        flavors.append(FlavorWrite(**data, projects=projects))
    return flavors


def get_images(conn: Connection) -> List[ImageWrite]:
    logger.info("Retrieve current project accessible images")
    images = []
    for image in conn.image.images(status="active"):
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
        data["is_public"] = is_public
        images.append(ImageWrite(**data, projects=projects))
    return images


def get_networks(conn: Connection) -> List[NetworkWrite]:
    logger.info("Retrieve current project accessible networks")
    networks = []
    for network in conn.network.networks(status="active"):
        project = None
        if not network.is_shared:
            project = conn.current_project_id
        data = network.to_dict()
        data["uuid"] = data.pop("id")
        if data.get("description") is None:
            data["description"] = ""
        if data.get("is_default") is None:
            data["is_default"] = False
        networks.append(NetworkWrite(**data, project=project))
    return networks


def get_project(conn: Connection) -> ProjectWrite:
    logger.info("Retrieve current project data")
    project = conn.identity.get_project(conn.current_project_id)
    data = project.to_dict()
    data["uuid"] = data.pop("id")
    if data.get("description") is None:
        data["description"] = ""
    return ProjectWrite(**data)


def get_correct_idp_and_user_group_for_project(
    *,
    trusted_idps: List[TrustedIDPOut],
    os_conf_auth_methods: List[AuthMethod],
    project_conf: OsProject,
) -> TrustedIDPOut:
    for trusted_idp in trusted_idps:
        for user_group in trusted_idp.user_groups:
            for sla in user_group.slas:
                if sla.doc_uuid == project_conf.sla:
                    if project_conf.id not in sla.projects:
                        sla.projects.append(project_conf.id)
                        for auth_method in os_conf_auth_methods:
                            if auth_method.endpoint == trusted_idp.endpoint:
                                trusted_idp.relationship = auth_method
                                return trusted_idp
                    return trusted_idp

    logger.error(
        "Configuration error: No matching Identity Provider "
        f"for project {project_conf.id}"
    )
    raise


def get_provider(
    *, os_conf: Openstack, trusted_idps: List[TrustedIDPOut]
) -> ProviderWrite:
    """Generate an Openstack virtual provider, reading information from a real
    openstack instance."""
    trust_idps = copy.deepcopy(trusted_idps)
    provider = ProviderWrite(
        name=os_conf.name,
        type=os_conf.type,
        is_public=os_conf.is_public,
        support_emails=os_conf.support_emails,
        status=os_conf.status,
    )

    for region_conf in os_conf.regions:
        region = RegionWrite(**region_conf.dict())

        for project_conf in os_conf.projects:
            trusted_idp = get_correct_idp_and_user_group_for_project(
                os_conf_auth_methods=os_conf.identity_providers,
                trusted_idps=trust_idps,
                project_conf=project_conf,
            )
            if trusted_idp is None:
                logger.error(f"Skipping project {project_conf.id}.")
                continue

            logger.info(
                f"Connecting through IDP {trusted_idp.endpoint} to openstack "
                f"'{os_conf.name}' and region '{region_conf.name}'. "
                f"Accessing with project ID: {project_conf.id}"
            )
            conn = connect(
                auth_url=os_conf.auth_url,
                auth_type="v3oidcaccesstoken",
                identity_provider=trusted_idp.relationship.idp_name,
                protocol=trusted_idp.relationship.protocol,
                access_token=trusted_idp.token,
                project_id=project_conf.id.hex,
                region_name=region_conf.name,
                timeout=TIMEOUT,
            )
            logger.info("Connected.")

            # Create region's compute service.
            # Retrieve flavors, images and current project corresponding quotas.
            # Add them to the compute service.
            compute_service = ComputeServiceWrite(
                endpoint=conn.compute.get_endpoint(),
                type=conn.compute.service_type,
                name="org.openstack.nova",
            )
            compute_service.flavors = get_flavors(conn)
            compute_service.images = get_images(conn)
            compute_service.quotas = [get_compute_quotas(conn)]
            q = get_per_user_compute_quotas(
                project=project_conf, curr_region=region.name
            )
            if q is not None:
                compute_service.quotas.append(q)

            for i, region_service in enumerate(region.compute_services):
                if region_service.endpoint == compute_service.endpoint:
                    uuids = [j.uuid for j in region_service.flavors]
                    region.compute_services[i].flavors += list(
                        filter(lambda x: x.uuid not in uuids, compute_service.flavors)
                    )
                    uuids = [j.uuid for j in region_service.images]
                    region.compute_services[i].images += list(
                        filter(lambda x: x.uuid not in uuids, compute_service.images)
                    )
                    region.compute_services[i].quotas += compute_service.quotas
                    break
            else:
                region.compute_services.append(compute_service)

            # Retrieve project's block storage service.
            # Remove last part which corresponds to the project ID.
            # Retrieve current project corresponding quotas.
            # Add them to the block storage service.
            endpoint = conn.block_storage.get_endpoint()
            endpoint = os.path.dirname(endpoint)
            block_storage_service = BlockStorageServiceWrite(
                endpoint=endpoint,
                type=conn.block_storage.service_type,
                name="org.openstack.cinder",
            )
            block_storage_service.quotas = [get_block_storage_quotas(conn)]
            q = get_per_user_block_storage_quotas(
                project=project_conf, curr_region=region.name
            )
            if q is not None:
                block_storage_service.quotas.append(q)

            for i, region_service in enumerate(region.block_storage_services):
                if region_service.endpoint == block_storage_service.endpoint:
                    region.block_storage_services[
                        i
                    ].quotas += block_storage_service.quotas
                    break
            else:
                region.block_storage_services.append(block_storage_service)

            # Retrieve region's network service.
            network_service = NetworkServiceWrite(
                endpoint=conn.network.get_endpoint(),
                type=conn.network.service_type,
                name="org.openstack.neutron",
            )
            network_service.networks = get_networks(conn)
            for i, region_service in enumerate(region.network_services):
                if region_service.endpoint == network_service.endpoint:
                    uuids = [j.uuid for j in region_service.networks]
                    region.network_services[i].networks += list(
                        filter(lambda x: x.uuid not in uuids, network_service.networks)
                    )
                    break
            else:
                region.network_services.append(network_service)

            # Retrieve provider's identity service.
            identity_service = IdentityServiceWrite(
                endpoint=os_conf.auth_url,
                type=conn.identity.service_type,
                name="org.openstack.keystone",
            )
            for region_service in region.identity_services:
                if region_service.endpoint == identity_service.endpoint:
                    break
            else:
                region.identity_services.append(identity_service)

            # Create project entity
            project = get_project(conn)
            if project.uuid not in [i.uuid for i in provider.projects]:
                provider.projects.append(project)

            conn.close()
            logger.info("Connection closed")

        provider.regions.append(region)

    # Filter on IDPs and user groups with SLAs
    # belonging to at least one project
    for idp in trust_idps:
        for user_group in idp.user_groups:
            user_group.slas = list(
                filter(lambda sla: len(sla.projects) > 0, user_group.slas)
            )
        idp.user_groups = list(
            filter(lambda user_group: len(user_group.slas) > 0, idp.user_groups)
        )
    provider.identity_providers = list(
        filter(lambda idp: len(idp.user_groups) > 0, trust_idps)
    )

    return provider
