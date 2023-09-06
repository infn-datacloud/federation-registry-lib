import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import yaml
from openstack import connect
from openstack.connection import Connection
from pydantic import UUID4, AnyHttpUrl, BaseModel, root_validator

external_path = Path.cwd().parent
sys.path.insert(1, str(external_path))

from app.auth_method.schemas import AuthMethodCreate
from app.flavor.schemas import FlavorCreate
from app.image.schemas import ImageCreate
from app.location.schemas import LocationBase
from app.project.schemas import ProjectCreate
from app.provider.schemas import ProviderBase
from app.provider.schemas_extended import (
    IdentityProviderCreateExtended,
    ProviderCreateExtended,
)

# openstack.enable_logging(True, stream=sys.stdout)

PREFERRED_IDP_LIST = ["https://iam.cloud.infn.it/"]


class IDP(BaseModel):
    name: str
    protocol: str
    group_claim: str
    endpoint: AnyHttpUrl


class Project(BaseModel):
    id: Optional[str]
    name: Optional[str]
    domain: Optional[str]

    @root_validator(pre=True)
    def check_id_or_name_and_domain(cls, values):
        if values.get("id") is not None:
            values["name"] = None
            values["domain"] = None
        else:
            assert (
                values["name"] is not None and values["domain"] is not None
            ), "If ID is None, both 'name' and 'domain' must be set"
        return {**values}


class OpenstackConfig(ProviderBase):
    auth_url: str
    location: LocationBase
    identity_providers: List[IDP]
    projects: List[Project]


class Config(BaseModel):
    openstack: List[OpenstackConfig]


def get_project_from_openstack(conn: Connection) -> ProjectCreate:
    curr_proj_id = conn.current_project.get("id")
    project = conn.identity.get_project(curr_proj_id)
    data = project.to_dict()
    data["uuid"] = data.pop("id")
    return ProjectCreate(**data)


def get_flavors_from_openstack(
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


def get_images_from_openstack(
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


def get_identity_providers_from_config(
    idp_list: List[IDP],
) -> List[IdentityProviderCreateExtended]:
    identity_providers = []
    for idp in idp_list:
        identity_providers.append(
            IdentityProviderCreateExtended(
                endpoint=idp.endpoint,
                group_claim=idp.group_claim,
                relationship=AuthMethodCreate(idp_name=idp.name, protocol=idp.protocol),
            )
        )
    return identity_providers


def choose_idp(
    identity_providers: List[IdentityProviderCreateExtended],
) -> IdentityProviderCreateExtended:
    for idp_url in PREFERRED_IDP_LIST:
        for chosen_idp in identity_providers:
            if idp_url == chosen_idp.endpoint:
                return chosen_idp


def generate_token(endpoint: AnyHttpUrl) -> str:
    return None


if __name__ == "__main__":
    tokens = {}

    with open("config.yaml") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        config = Config(**config)

    for v in config.openstack:
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
            print(project)
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

            provider.projects.append(get_project_from_openstack(conn))

            flavors, flav_proj = get_flavors_from_openstack(conn)
            uids = [j.uuid for j in provider.flavors]
            for i in flavors:
                if i.uuid not in uids:
                    provider.flavors.append(i)
            uids = flav_rels.keys()
            for k, v in flav_proj.items():
                if k not in uids:
                    flav_rels[k] = v

            images, imag_proj = get_images_from_openstack(conn)
            uids = [j.uuid for j in provider.images]
            for i in images:
                if i.uuid not in uids:
                    provider.images.append(i)
            uids = imag_rels.keys()
            for k, v in imag_proj.items():
                if k not in uids:
                    imag_rels[k] = v

            conn.close()

# print(provider)
# cmdb_url = "http://localhost:8000"

# print(conn.identity.projects())
# for project in conn.identity.projects():
#   print(project)

# resp = requests.post(
#    url=os.path.join(cmdb_url, "api/v1/providers/"),
#    data=provider,
#    headers={
#        "Authorization": "Bearer"
#    },
# )
# if resp.status_code != 201:
#    raise  # TODO
# print(resp.json())
#
# for service in conn.service_catalog:
#   print(service)
# for service in conn.list_services():
#    print(service)

# for image in conn.image.images():
# print(image)
#    print(image.to_dict().keys())
#    for k,v in image.to_dict().items():
#        print(f"{k}: {v}")
# for project in conn.identity.projects():
#    print(project)
# for idp in conn.identity.identity_providers():
#    print(idp)
