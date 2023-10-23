from typing import Any, List, Optional, Union
from uuid import UUID

from app.auth_method.schemas import AuthMethodCreate, AuthMethodRead
from app.flavor.schemas import FlavorCreate, FlavorRead, FlavorReadPublic
from app.identity_provider.schemas import (
    IdentityProviderCreate,
    IdentityProviderRead,
    IdentityProviderReadPublic,
)
from app.image.schemas import ImageCreate, ImageRead, ImageReadPublic
from app.location.schemas import LocationCreate, LocationRead, LocationReadPublic
from app.network.schemas import NetworkCreate, NetworkRead, NetworkReadPublic
from app.project.schemas import ProjectCreate, ProjectRead
from app.provider.schemas import ProviderCreate, ProviderRead, ProviderReadPublic
from app.quota.schemas import (
    BlockStorageQuotaCreate,
    BlockStorageQuotaRead,
    BlockStorageQuotaReadPublic,
    ComputeQuotaCreate,
    ComputeQuotaRead,
    ComputeQuotaReadPublic,
)
from app.region.schemas import RegionCreate, RegionRead, RegionReadPublic
from app.service.schemas import (
    BlockStorageServiceCreate,
    BlockStorageServiceRead,
    BlockStorageServiceReadPublic,
    ComputeServiceCreate,
    ComputeServiceRead,
    ComputeServiceReadPublic,
    IdentityServiceCreate,
    IdentityServiceRead,
    IdentityServiceReadPublic,
    NetworkServiceCreate,
    NetworkServiceRead,
    NetworkServiceReadPublic,
)
from app.sla.schemas import SLACreate, SLARead, SLAReadPublic
from app.user_group.schemas import UserGroupCreate, UserGroupRead, UserGroupReadPublic
from pydantic import Field, root_validator, validator


class UserGroupReadExtended(UserGroupRead):
    slas: List[SLARead] = Field(default_factory=list, description="List of SLA")


class UserGroupReadExtendedPublic(UserGroupReadPublic):
    slas: List[SLAReadPublic] = Field(default_factory=list, description="List of SLA")


class IdentityProviderReadExtended(IdentityProviderRead):
    """Model to extend the Identity Provider data read from the DB with the
    authentication method details."""

    relationship: AuthMethodRead = Field(
        description="Authentication method used by the Provider"
    )
    user_groups: List[UserGroupReadExtended] = Field(
        default_factory=list, description="List of owned users"
    )


class IdentityProviderReadExtendedPublic(IdentityProviderReadPublic):
    """Model to extend the Identity Provider data read from the DB with the
    authentication method details."""

    relationship: AuthMethodRead = Field(
        description="Authentication method used by the Provider"
    )
    user_groups: List[UserGroupReadExtendedPublic] = Field(
        default_factory=list, description="List of owned users"
    )


class BlockStorageServiceReadExtended(BlockStorageServiceRead):
    quotas: List[BlockStorageQuotaRead] = Field(
        default_factory=list, description="List of quotas"
    )


class BlockStorageServiceReadExtendedPublic(BlockStorageServiceReadPublic):
    quotas: List[BlockStorageQuotaReadPublic] = Field(
        default_factory=list, description="List of quotas"
    )


class ComputeServiceReadExtended(ComputeServiceRead):
    flavors: List[FlavorRead] = Field(
        default_factory=list, description="List of owned flavors"
    )
    images: List[ImageRead] = Field(
        default_factory=list, description="List of owned images"
    )
    quotas: List[ComputeQuotaRead] = Field(
        default_factory=list, description="List of quotas"
    )


class ComputeServiceReadExtendedPublic(ComputeServiceReadPublic):
    flavors: List[FlavorReadPublic] = Field(
        default_factory=list, description="List of owned flavors"
    )
    images: List[ImageReadPublic] = Field(
        default_factory=list, description="List of owned images"
    )
    quotas: List[ComputeQuotaReadPublic] = Field(
        default_factory=list, description="List of quotas"
    )


class NetworkServiceReadExtended(NetworkServiceRead):
    networks: List[NetworkRead] = Field(
        default_factory=list, description="List of owned networks"
    )


class NetworkServiceReadExtendedPublic(NetworkServiceReadPublic):
    networks: List[NetworkReadPublic] = Field(
        default_factory=list, description="List of owned networks"
    )


class RegionReadExtended(RegionRead):
    location: Optional[LocationRead] = Field(
        default=None, description="Region geographical location"
    )
    services: List[
        Union[
            BlockStorageServiceReadExtended,
            ComputeServiceReadExtended,
            IdentityServiceRead,
            NetworkServiceReadExtended,
        ]
    ] = Field(default_factory=list, description="List of hosted Services.")


class RegionReadExtendedPublic(RegionReadPublic):
    location: Optional[LocationReadPublic] = Field(
        default=None, description="Region geographical location"
    )
    services: List[
        Union[
            BlockStorageServiceReadExtendedPublic,
            ComputeServiceReadExtendedPublic,
            IdentityServiceReadPublic,
            NetworkServiceReadExtendedPublic,
        ]
    ] = Field(default_factory=list, description="List of hosted Services.")


class ProviderReadExtended(ProviderRead):
    """Model to extend the Provider data read from the DB with the lists of
    related items for authenticated users."""

    identity_providers: List[IdentityProviderReadExtended] = Field(
        default_factory=list,
        description="List of supported identity providers.",
    )
    projects: List[ProjectRead] = Field(
        default_factory=list, description="List of owned Projects."
    )
    regions: List[RegionReadExtended] = Field(
        default_factory=list, description="List of available regions"
    )


class ProviderReadExtendedPublic(ProviderReadPublic):
    """Model to extend the Provider data read from the DB with the lists of
    related items for non-authenticated users."""

    identity_providers: List[IdentityProviderReadExtendedPublic] = Field(
        default_factory=list,
        description="List of supported identity providers.",
    )
    projects: List[ProjectRead] = Field(
        default_factory=list, description="List of owned Projects."
    )
    regions: List[RegionReadExtendedPublic] = Field(
        default_factory=list, description="List of available regions"
    )


# CREATE CLASSES


def find_duplicates(items: Any, attr: Optional[str] = None) -> None:
    """Find duplicate items in a list.

    Optionally filter items by attribute
    """
    if attr:
        values = [j.__getattribute__(attr) for j in items]
    else:
        values = items
    seen = set()
    dupes = [x for x in values if x in seen or seen.add(x)]
    if attr:
        assert (
            len(dupes) == 0
        ), f"There are multiple items with identical {attr}: {','.join(dupes)}"
    else:
        assert len(dupes) == 0, f"There are multiple identical items: {','.join(dupes)}"


class SLACreateExtended(SLACreate):
    project: str = Field(description="Project UUID")

    @validator("project", pre=True)
    def validate_projects(cls, v):
        if isinstance(v, UUID):
            return v.hex
        return v


class UserGroupCreateExtended(UserGroupCreate):
    sla: SLACreateExtended = Field(description="SLA related to this provider")


class IdentityProviderCreateExtended(IdentityProviderCreate):
    """Model to extend the Identity Provider data used to create a new instance
    in the DB with the authentication method details."""

    relationship: AuthMethodCreate = Field(
        description="Authentication method used by the Provider"
    )
    user_groups: List[UserGroupCreateExtended] = Field(
        description="List of user groups belonging to this identity provider",
    )

    @validator("user_groups")
    def validate_user_groups(cls, v):
        find_duplicates(v, "name")
        assert len(v), "Identity provider's user group list can't be empty"
        return v


class BlockStorageQuotaCreateExtended(BlockStorageQuotaCreate):
    project: str = Field(description="Project UUID")

    @validator("project", pre=True)
    def to_string(cls, v):
        if isinstance(v, UUID):
            return v.hex
        return v


class ComputeQuotaCreateExtended(ComputeQuotaCreate):
    project: str = Field(description="Project UUID")

    @validator("project", pre=True)
    def to_string(cls, v):
        if isinstance(v, UUID):
            return v.hex
        return v


class FlavorCreateExtended(FlavorCreate):
    projects: List[str] = Field(
        default_factory=list,
        description="List of projects having access to the private flavor",
    )

    @validator("projects", pre=True)
    def validate_projects(cls, v):
        v = [i.hex if isinstance(i, UUID) else i for i in v]
        find_duplicates(v)
        return v

    @root_validator
    def project_require_if_private_flavor(cls, values):
        if not values.get("is_public"):
            assert len(
                values.get("projects", [])
            ), "Projects are mandatory for private flavors"
        else:
            assert not len(
                values.get("projects", [])
            ), "Public flavors do not have linked projects"
        return values


class ImageCreateExtended(ImageCreate):
    projects: List[str] = Field(
        default_factory=list,
        description="List of projects having access to the private image",
    )

    @validator("projects", pre=True)
    def validate_projects(cls, v):
        v = [i.hex if isinstance(i, UUID) else i for i in v]
        find_duplicates(v)
        return v

    @root_validator
    def project_require_if_private_image(cls, values):
        if not values.get("is_public"):
            assert len(
                values.get("projects", [])
            ), "Projects are mandatory for private images"
        else:
            assert not len(
                values.get("projects", [])
            ), "Public images do not have linked projects"
        return values


class NetworkCreateExtended(NetworkCreate):
    project: Optional[str] = Field(
        default=None, description="Project having access to a private net"
    )

    @validator("project", pre=True)
    def to_string(cls, v):
        if isinstance(v, UUID):
            return v.hex
        return v

    @root_validator
    def project_require_if_private_net(cls, values):
        if not values.get("is_shared"):
            assert values.get("project") is not None
        else:
            assert values.get("project") is None
        return values


class BlockStorageServiceCreateExtended(BlockStorageServiceCreate):
    quotas: List[BlockStorageQuotaCreateExtended] = Field(
        default_factory=list, description="List or related quotas"
    )

    @validator("quotas")
    def max_two_quotas_on_same_project(cls, v: List[BlockStorageQuotaCreateExtended]):
        d = {}
        for quota in v:
            if quota.project is not None:
                msg = f"Multiple quotas on same project {quota.project}"
                q = d.get(quota.project)
                if q is None:
                    d[quota.project] = [1, quota.per_user]
                else:
                    q[0] += 1
                    assert q[0] <= 2 and q[1] != quota.per_user, msg
        return v


class ComputeServiceCreateExtended(ComputeServiceCreate):
    flavors: List[FlavorCreateExtended] = Field(
        default_factory=list,
        description="List of flavors accessible through this service",
    )
    images: List[ImageCreateExtended] = Field(
        default_factory=list,
        description="List of images accessible through this service",
    )
    quotas: List[ComputeQuotaCreateExtended] = Field(
        default_factory=list, description="List or related quotas"
    )

    @validator("flavors")
    def validate_flavors(cls, v):
        find_duplicates(v, "uuid")
        find_duplicates(v, "name")
        return v

    @validator("images")
    def validate_images(cls, v):
        find_duplicates(v, "uuid")
        find_duplicates(v, "name")
        return v

    @validator("quotas")
    def max_two_quotas_on_same_project(cls, v: List[BlockStorageQuotaCreateExtended]):
        d = {}
        for quota in v:
            if quota.project is not None:
                msg = f"Multiple quotas on same project {quota.project}"
                q = d.get(quota.project)
                if q is None:
                    d[quota.project] = [1, quota.per_user]
                else:
                    q[0] += 1
                    assert q[0] <= 2 and q[1] != quota.per_user, msg
        return v


class NetworkServiceCreateExtended(NetworkServiceCreate):
    networks: List[NetworkCreateExtended] = Field(
        default_factory=list,
        description="List of networks accessible through this service",
    )

    @validator("networks")
    def validate_networks(cls, v):
        find_duplicates(v, "uuid")
        return v


class RegionCreateExtended(RegionCreate):
    location: Optional[LocationCreate] = Field(
        default=None, description="Geographical site"
    )
    block_storage_services: List[BlockStorageServiceCreateExtended] = Field(
        default_factory=list, description="Block storage service"
    )
    compute_services: List[ComputeServiceCreateExtended] = Field(
        default_factory=list, description="Compute service"
    )
    identity_services: List[IdentityServiceCreate] = Field(
        default_factory=list, description="Identity service"
    )
    network_services: List[NetworkServiceCreateExtended] = Field(
        default_factory=list, description="Network service"
    )

    @validator("block_storage_services")
    def validate_block_storage_services(cls, v):
        find_duplicates(v, "endpoint")
        return v

    @validator("compute_services")
    def validate_compute_services(cls, v):
        find_duplicates(v, "endpoint")
        return v

    @validator("identity_services")
    def validate_identity_services(cls, v):
        find_duplicates(v, "endpoint")
        return v

    @validator("network_services")
    def validate_network_services(cls, v):
        find_duplicates(v, "endpoint")
        return v


class ProviderCreateExtended(ProviderCreate):
    """Model to extend the Provider data used to create a new instance in the
    DB with the lists of related items."""

    identity_providers: List[IdentityProviderCreateExtended] = Field(
        default_factory=list,
        description="List of supported identity providers.",
    )
    projects: List[ProjectCreate] = Field(
        default_factory=list, description="List of owned Projects."
    )
    regions: List[RegionCreateExtended] = Field(
        default_factory=list, description="Provider regions."
    )

    @validator("identity_providers")
    def validate_identity_providers(cls, v: List[IdentityProviderCreateExtended]):
        find_duplicates(v, "endpoint")
        return v

    @validator("projects")
    def validate_projects(cls, v):
        find_duplicates(v, "uuid")
        find_duplicates(v, "name")
        return v

    @validator("regions")
    def validate_regions(cls, v):
        find_duplicates(v, "name")
        return v

    @root_validator
    def check_referenced_projects_exist(cls, values):
        projects = [i.uuid for i in values.get("projects", [])]
        seen = set()
        for identity_provider in values.get("identity_providers", []):
            for user_group in identity_provider.user_groups:
                assert (
                    user_group.sla.doc_uuid not in seen
                ), f"SLA {user_group.sla.doc_uuid} already used by another user group"
                seen.add(user_group.sla.doc_uuid)

                msg = (
                    f"SLA {user_group.sla.doc_uuid}'s project {user_group.sla.project} "
                )
                msg += f"not in this provider: {projects}"
                assert user_group.sla.project in projects, msg

        for region in values.get("regions", []):
            for service in region.block_storage_services:
                for quota in service.quotas:
                    if quota.project is not None:
                        msg = f"Block storage quota's project {quota.project} "
                        msg += f"not in this provider: {projects}"
                        assert quota.project in projects, msg

            for service in region.compute_services:
                for flavor in service.flavors:
                    for project in flavor.projects:
                        msg = f"Flavor {flavor.name}'s project {project} "
                        msg += f"not in this provider: {projects}"
                        assert project in projects, msg
                for image in service.images:
                    for project in image.projects:
                        msg = f"Image {image.name}'s project {project} "
                        msg += f"not in this provider: {projects}"
                        assert project in projects, msg
                for quota in service.quotas:
                    if quota.project is not None:
                        msg = f"Compute quota's project {quota.project} "
                        msg += f"not in this provider: {projects}"
                        assert quota.project in projects, msg

            for service in region.network_services:
                for network in service.networks:
                    if network.project is not None:
                        msg = f"Network {network.name}'s project {network.project} "
                        msg += f"not in this provider: {projects}"
                        assert network.project in projects, msg

        return values
