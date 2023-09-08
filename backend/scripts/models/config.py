import sys
from pathlib import Path
from typing import List, Optional

from pydantic import AnyHttpUrl, BaseModel, Field, root_validator

external_path = Path.cwd().parent
sys.path.insert(1, str(external_path))

from app.location.schemas import LocationCreate
from app.provider.schemas import ProviderCreate


class IDP(BaseModel):
    name: str = Field(description="Identity provider name used to authenticate")
    protocol: str = Field(description="Protocol used to authenticate")
    group_claim: str = Field(
        description="Key name from which derive user's authorization"
    )
    endpoint: AnyHttpUrl = Field(description="Identity provider endpoint")


class Project(BaseModel):
    id: Optional[str] = Field(default=None, description="Project unique ID")
    name: Optional[str] = Field(default=None, description="Project name")
    domain: Optional[str] = Field(default=None, description="Project domain name")

    @root_validator
    def check_id_or_name_and_domain(cls, values):
        if values.get("id") is not None:
            values["name"] = None
            values["domain"] = None
        else:
            assert (
                values["name"] is not None and values["domain"] is not None
            ), "If ID is None, both 'name' and 'domain' must be set"
        return values


class Openstack(ProviderCreate):
    auth_url: str = Field(description="Identity service endpoint")
    location: LocationCreate = Field(description="Location details")
    identity_providers: List[IDP] = Field(
        description="List of supported identity providers"
    )
    projects: List[Project] = Field(description="List of projects to inspect")


class CMDB(BaseModel):
    url: AnyHttpUrl = Field(description="CMDB base URL")
    api_ver_flavors: str = Field(default="v1", description="Flavors API version to use")
    api_ver_identity_providers: str = Field(
        default="v1", description="Identity providers API version to use"
    )
    api_ver_images: str = Field(default="v1", description="Images API version to use")
    api_ver_locations: str = Field(
        default="v1", description="Locations API version to use"
    )
    api_ver_projects: str = Field(
        default="v1", description="Projects API version to use"
    )
    api_ver_providers: str = Field(
        default="v1", description="Providers API version to use"
    )
    api_ver_services: str = Field(
        default="v1", description="Services API version to use"
    )
    api_ver_slas: str = Field(default="v1", description="SLAs API version to use")
    api_ver_user_groups: str = Field(
        default="v1", description="User groups API version to use"
    )


class Config(BaseModel):
    cmdb: CMDB = Field(description="CMDB configuration parameters")
    oidc_agent_accounts: List[AnyHttpUrl] = Field(
        description="List of OIDC-Agent supported identity providers endpoints"
    )
    openstack: List[Openstack] = Field(
        description="List of openstack providers to integrate in the CMDB"
    )
