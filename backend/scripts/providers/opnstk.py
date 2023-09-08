from typing import List

from models.cmdb import AuthMethod, Flavor, IdentityProvider, Image, Project, Provider
from models.config import IDP, Openstack
from openstack import connect
from openstack.connection import Connection


def get_project(conn: Connection) -> Project:
    curr_proj_id = conn.current_project.get("id")
    project = conn.identity.get_project(curr_proj_id)
    data = project.to_dict()
    data["uuid"] = data.pop("id")
    if data.get("description") is None:
        data["description"] = ""
    return Project(**data)


def get_flavors(conn: Connection) -> List[Flavor]:
    flavors = []
    for flavor in conn.compute.flavors():
        projects = []
        if not flavor.is_public:
            projects = conn.compute.get_flavor_access(flavor)
        data = flavor.to_dict()
        data["uuid"] = data.pop("id")
        if data.get("description") is None:
            data["description"] = ""
        flavors.append(Flavor(**data, projects=projects))
    return flavors


def get_images(conn: Connection) -> List[Image]:
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
        images.append(Image(**data, projects=projects))
    return images


def get_identity_providers_from_config(
    idp_list: List[IDP],
) -> List[IdentityProvider]:
    identity_providers = []
    for idp in idp_list:
        identity_providers.append(
            IdentityProvider(
                endpoint=idp.endpoint,
                group_claim=idp.group_claim,
                relationship=AuthMethod(idp_name=idp.name, protocol=idp.protocol),
            )
        )
    return identity_providers


def get_os_provider(*, config: Openstack, chosen_idp: IDP, token: str) -> Provider:
    """Generate an Openstack virtual provider, reading information from a real
    openstack instance."""
    provider = Provider(
        name=config.name,
        is_public=config.is_public,
        support_emails=config.support_emails,
        location=config.location,
        identity_providers=get_identity_providers_from_config(
            config.identity_providers
        ),
    )

    for project in config.projects:
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

        conn.close()

    return provider
