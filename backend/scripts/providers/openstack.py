import sys
from pathlib import Path
from typing import Dict, List, Tuple

from openstack import connect
from openstack.connection import Connection
from pydantic import UUID4
from scripts.models import Openstack
from utils import choose_idp, generate_token, get_identity_providers_from_config

external_path = Path.cwd().parent
sys.path.insert(1, str(external_path))

from app.flavor.schemas import FlavorCreate
from app.image.schemas import ImageCreate
from app.project.schemas import ProjectCreate
from app.provider.schemas_extended import ProviderCreateExtended


def get_project(conn: Connection) -> ProjectCreate:
    curr_proj_id = conn.current_project.get("id")
    project = conn.identity.get_project(curr_proj_id)
    data = project.to_dict()
    data["uuid"] = data.pop("id")
    return ProjectCreate(**data)


def get_flavors(
    conn: Connection,
) -> Tuple[List[FlavorCreate], Dict[UUID4, List[UUID4]]]:
    flavors = []
    flav_proj = {}
    for flavor in conn.compute.flavors():
        if not flavor.is_public:
            projects = conn.compute.get_flavor_access(flavor)
            flav_proj[flavor.id] = projects
        data = flavor.to_dict()
        data["uuid"] = data.pop("id")
        flavors.append(FlavorCreate(**data))
    return (flavors, flav_proj)


def get_images(
    conn: Connection,
) -> Tuple[List[ImageCreate], Dict[UUID4, List[UUID4]]]:
    images = []
    imag_proj = {}
    for image in conn.image.images():
        is_public = True
        if image.visibility in ["private", "shared"]:
            imag_proj[image.id] = [image.owner_id]
            is_public = False
        if image.visibility == "shared":
            members = list(conn.image.members(image))
            for member in members:
                if member.status == "accepted":
                    imag_proj[image.id].append(member.id)
        data = image.to_dict()
        data["uuid"] = data.pop("id")
        data["version"] = data.pop("os_version")
        data["distribution"] = data.pop("os_distro")
        data["is_public"] = is_public
        data.pop("visibility")
        images.append(ImageCreate(**data))
    return (images, imag_proj)


def create_os_provider(
    v: Openstack, tokens: Dict[UUID4, str]
) -> ProviderCreateExtended:
    auth_url = v.auth_url
    provider = ProviderCreateExtended(
        name=v.name,
        is_public=v.is_public,
        support_emails=v.support_emails,
        location=v.location,
    )
    provider.identity_providers = get_identity_providers_from_config(
        v.identity_providers
    )
    chosen_idp = choose_idp(provider.identity_providers)
    if tokens.get(chosen_idp.endpoint) is None:
        tokens[chosen_idp.endpoint] = generate_token(chosen_idp.endpoint)

    flav_rels = {}
    imag_rels = {}
    for project in v.projects:
        conn = connect(
            auth_url=auth_url,
            auth_type="v3oidcaccesstoken",
            identity_provider=chosen_idp.relationship.idp_name,
            protocol=chosen_idp.relationship.protocol,
            access_token=tokens[chosen_idp.endpoint],
            project_id=project.id,
            project_name=project.name,
            project_domain_name=project.domain,
        )

        provider.projects.append(get_project(conn))

        flavors, flav_proj = get_flavors(conn)
        uids = [j.uuid for j in provider.flavors]
        for i in flavors:
            if i.uuid not in uids:
                provider.flavors.append(i)
        uids = flav_rels.keys()
        for k, v in flav_proj.items():
            if k not in uids:
                flav_rels[k] = v

        images, imag_proj = get_images(conn)
        uids = [j.uuid for j in provider.images]
        for i in images:
            if i.uuid not in uids:
                provider.images.append(i)
        uids = imag_rels.keys()
        for k, v in imag_proj.items():
            if k not in uids:
                imag_rels[k] = v

        conn.close()

    return provider
