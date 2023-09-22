from typing import List, Optional, Union

from app.identity_provider.schemas import IdentityProviderBase
from app.location.schemas import LocationBase
from app.provider.schemas import ProviderBase
from app.quota.schemas import BlockStorageQuotaBase, ComputeQuotaBase
from app.region.schemas import RegionBase
from app.sla.schemas import SLABase
from app.user_group.schemas import UserGroupBase
from pydantic import AnyHttpUrl, BaseModel, Field, root_validator, validator


class IdentityProvider(IdentityProviderBase):
    name: str = Field(description="Identity provider name used to authenticate")
    protocol: str = Field(description="Protocol used to authenticate")


class Limits(BaseModel):
    block_storage: Optional[BlockStorageQuotaBase] = Field(
        default=None, description="Block storage per user quota"
    )
    compute: Optional[ComputeQuotaBase] = Field(
        default=None, description="Compute per user quota"
    )

    @validator("block_storage")
    def set_per_user_block_storage(
        cls, v: Optional[BlockStorageQuotaBase]
    ) -> Optional[BlockStorageQuotaBase]:
        if v is not None:
            v.per_user = True
        return v

    @validator("compute")
    def set_per_user_compute(
        cls, v: Optional[ComputeQuotaBase]
    ) -> Optional[ComputeQuotaBase]:
        if v is not None:
            v.per_user = True
        return v


class UserGroup(UserGroupBase):
    idp: Union[str, AnyHttpUrl] = Field(description="Identity provider name or URL")


class PrivateNetProxy(BaseModel):
    ip: str = Field(description="Proxy IP address")
    user: str = Field(description="Username to use when performing ssh operations")


class RegionProps(BaseModel):
    region_name: str = Field(description="Region name")
    default_public_net: Optional[str] = Field(
        default=None, description="Name of the default public network"
    )
    default_private_net: Optional[str] = Field(
        default=None, description="Name of the default private network"
    )
    private_net_proxy: Optional[PrivateNetProxy] = Field(
        default=None, description="Proxy details to use to access to private network"
    )
    per_user_limits: Optional[Limits] = Field(
        default=None,
        description="Quota limitations to apply to users owning this project",
    )


class Project(BaseModel):
    id: Optional[str] = Field(default=None, description="Project unique ID")
    name: Optional[str] = Field(default=None, description="Project name")
    domain: Optional[str] = Field(default=None, description="Project domain name")
    group: UserGroup = Field(description="User group having access to this project")
    default_public_net: Optional[str] = Field(
        default=None, description="Name of the default public network"
    )
    default_private_net: Optional[str] = Field(
        default=None, description="Name of the default private network"
    )
    private_net_proxy: Optional[PrivateNetProxy] = Field(
        default=None, description="Proxy details to use to access to private network"
    )
    per_user_limits: Optional[Limits] = Field(
        default=None,
        description="Quota limitations to apply to users owning this project",
    )
    per_region_props: List[RegionProps] = Field(
        default_factory=list, description="Region specific properties"
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


class Region(RegionBase):
    location: LocationBase = Field(description="Location details")


class Openstack(ProviderBase):
    auth_url: str = Field(description="Identity service endpoint")
    identity_providers: List[IdentityProvider] = Field(
        description="List of supported identity providers"
    )
    regions: List[Region] = Field(description="List of hosted regions")
    slas: List[SLA] = Field(description="List of SLAs belonged by this provider")


class APIVersions(BaseModel):
    flavors: str = Field(default="v1", description="Flavors API version to use")
    identity_providers: str = Field(
        default="v1", description="Identity providers API version to use"
    )
    images: str = Field(default="v1", description="Images API version to use")
    locations: str = Field(default="v1", description="Locations API version to use")
    networks: str = Field(default="v1", description="Networks API version to use")
    projects: str = Field(default="v1", description="Projects API version to use")
    providers: str = Field(default="v1", description="Providers API version to use")
    regions: str = Field(default="v1", description="Regions API version to use")
    quotas: str = Field(default="v1", description="Quotas API version to use")
    services: str = Field(default="v1", description="Services API version to use")
    slas: str = Field(default="v1", description="SLAs API version to use")
    user_groups: str = Field(default="v1", description="User groups API version to use")


class CMDB(BaseModel):
    base_url: AnyHttpUrl = Field(description="CMDB base URL")
    api_ver: APIVersions = Field(description="API versions")


class ConfigIn(BaseModel):
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
    networks: AnyHttpUrl = Field(description="Networks endpoint")
    projects: AnyHttpUrl = Field(description="Projects endpoint")
    providers: AnyHttpUrl = Field(description="Providers endpoint")
    regions: AnyHttpUrl = Field(description="Regions endpoint")
    quotas: AnyHttpUrl = Field(description="Quotas endpoint")
    services: AnyHttpUrl = Field(description="Services endpoint")
    slas: AnyHttpUrl = Field(description="SLAs endpoint")
    user_groups: AnyHttpUrl = Field(description="User Groups endpoint")


class ConfigOut(BaseModel):
    cmdb_urls: URLs = Field(description="CMDB endpoints to use")
    oidc_agent_accounts: List[AnyHttpUrl] = Field(
        description="List of OIDC-Agent supported identity providers endpoints"
    )
    openstack: List[Openstack] = Field(
        description="List of openstack providers to integrate in the CMDB"
    )
