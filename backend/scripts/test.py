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


class Proj(BaseModel):
    id: Optional[UUID4]
    name: Optional[str]
    domain: Optional[str]

    @root_validator
    def validate(cls, values):
        if values.get("id") is not None:
            values["name"] = None
            values["domain"] = None
        else:
            assert values["name"] is not None and values["domain"] is not None
        return values


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

    for k, v in config.get("openstack", {}).items():
        auth_url = v.get("auth_url")
        provider = ProviderCreateExtended(
            name=k,
            is_public=v.get("is_public"),
            support_emails=v.get("support_emails"),
            location=v.get("location"),
        )
        provider.identity_providers = get_identity_providers_from_config(
            [IDP(**p) for p in v.get("identity_providers", [])]
        )
        chosen_idp = choose_idp(provider.identity_providers)
        if tokens.get(chosen_idp.endpoint) is None:
            tokens[chosen_idp.endpoint] = generate_token(chosen_idp.endpoint)

        for project in [Proj(**p) for p in v.get("projects", [])]:
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

            flavors, flav_proj = get_flavors_from_openstack(conn)
            images, imag_proj = get_images_from_openstack(conn)

            provider["flavors"] |= set(flavors)
            provider["images"] |= set(images)

        print(provider)

#    provider = {}
#    provider["images"] = flavors
#    provider["images"] = images

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
