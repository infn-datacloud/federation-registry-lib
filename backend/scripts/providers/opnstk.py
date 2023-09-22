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
from models.cmdb.sla import SLAWrite
from models.cmdb.user_group import UserGroupWrite
from models.config import IdentityProvider, Openstack
from openstack import connect
from openstack.connection import Connection
from utils import (
    get_identity_providers,
    get_per_user_block_storage_quotas,
    get_per_user_compute_quotas,
)


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


def get_networks(conn: Connection) -> List[NetworkWrite]:
    logger.info("Retrieve current project accessible images")
    networks = []
    for network in conn.network.networks():
        # is_public = True
        # projects = []
        # if network.visibility in ["private", "shared"]:
        #    projects = [network.owner_id]
        #    is_public = False
        # if network.visibility == "shared":
        #    members = list(conn.network.members(network))
        #    for member in members:
        #        if member.status == "accepted":
        #            projects.append(member.id)
        data = network.to_dict()
        data["uuid"] = data.pop("id")
        if data.get("description") is None:
            data["description"] = ""
        # data["version"] = data.pop("os_version")
        # data["distribution"] = data.pop("os_distro")
        # data["is_public"] = is_public
        # data.pop("visibility")
        networks.append(NetworkWrite(**data))  # , projects=projects))
    return networks


def get_project(conn: Connection) -> ProjectWrite:
    logger.info("Retrieve current project data")
    project = conn.identity.get_project(conn.current_project_id)
    data = project.to_dict()
    data["uuid"] = data.pop("id")
    if data.get("description") is None:
        data["description"] = ""
    return ProjectWrite(**data)


def get_provider(
    *, obj_in: Openstack, chosen_idp: IdentityProvider, token: str
) -> ProviderWrite:
    """Generate an Openstack virtual provider, reading information from a real
    openstack instance."""
    provider = ProviderWrite(
        name=obj_in.name,
        is_public=obj_in.is_public,
        support_emails=obj_in.support_emails,
        status=obj_in.status,
        identity_providers=get_identity_providers(obj_in.identity_providers),
    )

    for conf_region in obj_in.regions:
        region = RegionWrite(**conf_region.dict())

        for conf_sla in obj_in.slas:
            if conf_sla.project.id is not None:
                logger.info(
                    "Connecting to openstack region: "
                    f"{obj_in.name} - {conf_region.name}."
                )
                logger.info(f"Accessing with project ID: {conf_sla.project.id}")
            else:
                logger.info(
                    "Connecting to openstack region: "
                    f"{obj_in.name} - {conf_region.name}."
                )
                logger.info(
                    "Accessing with project name and domain: "
                    f"{conf_sla.project.name} - {conf_sla.project.domain}"
                )
            conn = connect(
                auth_url=obj_in.auth_url,
                auth_type="v3oidcaccesstoken",
                identity_provider=chosen_idp.name,
                protocol=chosen_idp.protocol,
                access_token=token,
                project_id=conf_sla.project.id,
                project_name=conf_sla.project.name,
                project_domain_name=conf_sla.project.domain,
                region_name=conf_region.name,
            )
            if conf_sla.project.id is None:
                conf_sla.project.id = conn.current_project_id
            logger.info(f"Connected. Project ID: {conf_sla.project.id}")

            # Create SLA and user group.
            # Attach SLA to User group.
            # Append user group to corresponding identity provider.
            sla = SLAWrite(
                doc_uuid=conf_sla.doc_uuid,
                start_date=conf_sla.start_date,
                end_date=conf_sla.end_date,
                project=conn.current_project_id,
            )
            user_group = UserGroupWrite(name=conf_sla.project.group.name, sla=sla)
            for i, idp in enumerate(provider.identity_providers):
                if idp.endpoint == conf_sla.project.group.idp:
                    provider.identity_providers[i].user_groups.append(user_group)

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
                project=conf_sla.project, curr_region=region.name
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
            # Retrieve current project corresponding quotas.
            # Add them to the block storage service.
            block_storage_service = BlockStorageServiceWrite(
                endpoint=conn.block_storage.get_endpoint(),
                type=conn.block_storage.service_type,
                name="org.openstack.cinder",
            )
            block_storage_service.quotas = [get_block_storage_quotas(conn)]
            q = get_per_user_block_storage_quotas(
                project=conf_sla.project, curr_region=region.name
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
                endpoint=obj_in.auth_url,
                type=conn.identity.service_type,
                name="org.openstack.keystone",
            )
            for region_service in region.identity_services:
                if region_service.endpoint == identity_service.endpoint:
                    break
            else:
                region.block_storage_services.append(block_storage_service)

            # Create project entity
            provider.projects.append(get_project(conn))

            conn.close()
            logger.info("Connection closed")

        provider.regions.append(region)

    return provider
