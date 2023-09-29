import subprocess
from typing import List, Optional

from app.auth_method.schemas import AuthMethodBase
from app.identity_provider.schemas import IdentityProviderBase
from app.location.schemas import LocationBase
from app.provider.enum import ProviderType
from app.provider.schemas import ProviderBase
from app.quota.schemas import BlockStorageQuotaBase, ComputeQuotaBase
from app.region.schemas import RegionBase
from models.cmdb.user_group import UserGroupWrite
from pydantic import UUID4, AnyHttpUrl, BaseModel, Field, root_validator, validator


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


class TrustedIDPIn(IdentityProviderBase):
    issuer: AnyHttpUrl = Field(description="issuer url")
    user_groups: List[UserGroupWrite] = Field(
        default_factory=list, description="User groups"
    )

    @root_validator(pre=True)
    def rename_issuer_to_endpoint(cls, values):
        values["endpoint"] = values.get("issuer")
        return values


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


class PrivateNetProxy(BaseModel):
    ip: str = Field(description="Proxy IP address")
    user: str = Field(description="Username to use when performing ssh operations")


class PerRegionProps(BaseModel):
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


class AuthMethod(AuthMethodBase):
    idp_name: str = Field(
        alias="name", description="Identity provider name used to authenticate"
    )
    endpoint: AnyHttpUrl = Field(description="Identity Provider URL")


class BlockStorageVolMap(BaseModel):
    ...


class Project(BaseModel):
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
    per_region_props: List[PerRegionProps] = Field(
        default_factory=list, description="Region specific properties"
    )
    sla: UUID4 = Field(description="SLA document uuid")


class K8sNameSpace(Project):
    name: str = Field(default=None, description="Namespace string")


class OsProject(Project):
    id: UUID4 = Field(default=None, description="Project unique ID")


class Region(RegionBase):
    location: Optional[LocationBase] = Field(
        default=None, description="Location details"
    )


class Provider(ProviderBase):
    auth_url: AnyHttpUrl = Field(description="Identity service endpoint")
    block_storage_vol_types: Optional[BlockStorageVolMap] = Field(default=None)
    identity_providers: List[AuthMethod] = Field(
        description="List of supported identity providers"
    )


class Openstack(Provider):
    projects: List[OsProject] = Field(
        description="List of SLAs belonged by this provider"
    )
    regions: List[Region] = Field(description="List of hosted regions")
    type: ProviderType = Field(default="openstack", description="Provider type")
    image_tags: List[str] = Field(
        default_factory=list, description="List of image tags to filter"
    )
    network_tags: List[str] = Field(
        default_factory=list, description="List of network tags to filter"
    )


class Kubernetes(Provider):
    projects: List[K8sNameSpace] = Field(description="list fo name")
    regions: List[Region] = Field(
        default_factory=list, description="List of hosted regions"
    )
    type: ProviderType = Field(default="kubernetes", description="Provider type")


class ConfigIn(BaseModel):
    cmdb: CMDB = Field(description="CMDB configuration parameters")
    trusted_idps: List[TrustedIDPIn] = Field(
        description="List of OIDC-Agent supported identity providers endpoints"
    )
    openstack: List[Openstack] = Field(
        default_factory=list,
        description="List of openstack providers to integrate in the CMDB",
    )
    kubernetes: List[Kubernetes] = Field(
        default_factory=list,
        description="List of openstack providers to integrate in the CMDB",
    )


class TrustedIDPOut(IdentityProviderBase):
    user_groups: List[UserGroupWrite] = Field(
        default_factory=list, description="User groups"
    )
    relationship: Optional[AuthMethodBase] = Field(default=None, description="")
    token: str = Field(description="Access token")

    @root_validator(pre=True)
    def generate_token(cls, values):
        if values.get("token") is None:
            token_cmd = subprocess.run(
                [
                    "docker",
                    "exec",
                    "catalog-api-oidc-agent-1",
                    "oidc-token",
                    values.get("endpoint"),
                ],
                stdout=subprocess.PIPE,
                text=True,
            )
            values["token"] = token_cmd.stdout.strip("\n")
        return values


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
    trusted_idps: List[TrustedIDPOut] = Field(
        description="List of OIDC-Agent supported identity providers endpoints"
    )
    openstack: List[Openstack] = Field(
        default_factory=list,
        description="List of openstack providers to integrate in the CMDB",
    )
    kubernetes: List[Kubernetes] = Field(
        default_factory=list,
        description="List of openstack providers to integrate in the CMDB",
    )
