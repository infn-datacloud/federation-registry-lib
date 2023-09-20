from typing import List, Optional, Union

from app.identity_provider.schemas import IdentityProviderBase
from app.location.schemas import LocationCreate
from app.provider.schemas import ProviderCreate
from app.sla.schemas import SLABase
from app.user_group.schemas import UserGroupBase
from models.cmdb.quota import BlockStorageQuotaWrite, ComputeQuotaWrite
from pydantic import AnyHttpUrl, BaseModel, Field, root_validator, validator


class IDP(IdentityProviderBase):
    name: str = Field(description="Identity provider name used to authenticate")
    protocol: str = Field(description="Protocol used to authenticate")


class Limits(BaseModel):
    compute: Optional[ComputeQuotaWrite] = Field(
        default=None, description="Compute per user quota"
    )
    block_storage: Optional[BlockStorageQuotaWrite] = Field(
        default=None, description="Block storage per user quota"
    )

    @validator("compute")
    def set_per_user_compute(
        cls, v: Optional[ComputeQuotaWrite]
    ) -> Optional[ComputeQuotaWrite]:
        if v is not None:
            v.per_user = True
        return v

    @validator("block_storage")
    def set_per_user_block_storage(
        cls, v: Optional[BlockStorageQuotaWrite]
    ) -> Optional[BlockStorageQuotaWrite]:
        if v is not None:
            v.per_user = True
        return v


class UserGroup(UserGroupBase):
    idp: Union[str, AnyHttpUrl] = Field(description="Identity provider name or URL")


class Project(BaseModel):
    id: Optional[str] = Field(default=None, description="Project unique ID")
    name: Optional[str] = Field(default=None, description="Project name")
    domain: Optional[str] = Field(default=None, description="Project domain name")
    group: UserGroup = Field(description="User group having access to this project")
    per_user_limits: Optional[Limits] = Field(
        default=None,
        description="Quota limitations to apply to users owning this project",
    )
    # _region: Optional[str] = Field(default=None,
    # description="Service region to use to access to this project")

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


class SLA(SLABase):
    project: Project = Field(description="Linked project")


class Openstack(ProviderCreate):
    auth_url: str = Field(description="Identity service endpoint")
    location: LocationCreate = Field(description="Location details")
    identity_providers: List[IDP] = Field(
        description="List of supported identity providers"
    )
    slas: List[SLA] = Field(description="List of SLAs belonged by this provider")


class APIVersions(BaseModel):
    flavors: str = Field(default="v1", description="Flavors API version to use")
    identity_providers: str = Field(
        default="v1", description="Identity providers API version to use"
    )
    images: str = Field(default="v1", description="Images API version to use")
    locations: str = Field(default="v1", description="Locations API version to use")
    projects: str = Field(default="v1", description="Projects API version to use")
    providers: str = Field(default="v1", description="Providers API version to use")
    quotas: str = Field(default="v1", description="Quotas API version to use")
    services: str = Field(default="v1", description="Services API version to use")
    slas: str = Field(default="v1", description="SLAs API version to use")
    user_groups: str = Field(default="v1", description="User groups API version to use")


class CMDB(BaseModel):
    base_url: AnyHttpUrl = Field(description="CMDB base URL")
    api_ver: APIVersions = Field(description="API versions")


class Config(BaseModel):
    cmdb: CMDB = Field(description="CMDB configuration parameters")
    oidc_agent_accounts: List[AnyHttpUrl] = Field(
        description="List of OIDC-Agent supported identity providers endpoints"
    )
    openstack: List[Openstack] = Field(
        description="List of openstack providers to integrate in the CMDB"
    )


class URLs(BaseModel):
    flavors: AnyHttpUrl = Field(description="Flavors endpoint")
    identity_providers: AnyHttpUrl = Field(description="Identity Providers endpoint")
    images: AnyHttpUrl = Field(description="Images endpoint")
    locations: AnyHttpUrl = Field(description="Locations endpoint")
    projects: AnyHttpUrl = Field(description="Projects endpoint")
    providers: AnyHttpUrl = Field(description="Providers endpoint")
    quotas: AnyHttpUrl = Field(description="Quotas endpoint")
    services: AnyHttpUrl = Field(description="Services endpoint")
    slas: AnyHttpUrl = Field(description="SLAs endpoint")
    user_groups: AnyHttpUrl = Field(description="User Groups endpoint")
