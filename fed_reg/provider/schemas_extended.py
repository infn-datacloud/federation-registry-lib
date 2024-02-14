"""Pydantic extended models of the Resource Provider (openstack, kubernetes...)."""
from typing import Any, Dict, List, Optional, Union

from pydantic import Field, root_validator, validator

from fed_reg.auth_method.schemas import AuthMethodCreate, AuthMethodRead
from fed_reg.flavor.schemas import FlavorCreate, FlavorRead, FlavorReadPublic
from fed_reg.identity_provider.constants import DOC_EXT_GROUP
from fed_reg.identity_provider.schemas import (
    IdentityProviderCreate,
    IdentityProviderRead,
    IdentityProviderReadPublic,
)
from fed_reg.image.schemas import ImageCreate, ImageRead, ImageReadPublic
from fed_reg.location.schemas import (
    LocationCreate,
    LocationRead,
    LocationReadPublic,
)
from fed_reg.network.schemas import NetworkCreate, NetworkRead, NetworkReadPublic
from fed_reg.project.schemas import ProjectCreate, ProjectRead
from fed_reg.provider.constants import (
    DOC_EXT_AUTH_METH,
    DOC_EXT_IDP,
    DOC_EXT_PROJ,
    DOC_EXT_REG,
    DOC_NEW_GROUP,
    DOC_NEW_PROJ_UUID,
    DOC_NEW_PROJ_UUIDS,
    DOC_NEW_SERV_BLO_STO,
    DOC_NEW_SERV_COMP,
    DOC_NEW_SERV_ID,
    DOC_NEW_SERV_NET,
)
from fed_reg.provider.schemas import (
    ProviderCreate,
    ProviderRead,
    ProviderReadPublic,
)
from fed_reg.quota.schemas import (
    BlockStorageQuotaCreate,
    BlockStorageQuotaRead,
    BlockStorageQuotaReadPublic,
    ComputeQuotaCreate,
    ComputeQuotaRead,
    ComputeQuotaReadPublic,
    NetworkQuotaCreate,
    NetworkQuotaRead,
    NetworkQuotaReadPublic,
)
from fed_reg.region.constants import DOC_EXT_LOC, DOC_EXT_SERV
from fed_reg.region.schemas import RegionCreate, RegionRead, RegionReadPublic
from fed_reg.service.constants import (
    DOC_EXT_FLAV,
    DOC_EXT_IMAG,
    DOC_EXT_NETW,
    DOC_EXT_QUOTA,
)
from fed_reg.service.schemas import (
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
from fed_reg.sla.schemas import SLACreate, SLARead, SLAReadPublic
from fed_reg.user_group.constants import DOC_EXT_SLA
from fed_reg.user_group.schemas import (
    UserGroupCreate,
    UserGroupRead,
    UserGroupReadPublic,
)


class UserGroupReadExtended(UserGroupRead):
    """Model to extend the User Group data read from the DB.

    Attributes:
    ----------
        uid (int): User Group unique ID.
        description (str): Brief description.
        name (str): User Group name.
        slas (list of SLARead): Owned SLAs.
    """

    slas: List[SLARead] = Field(default_factory=list, description=DOC_EXT_SLA)


class UserGroupReadExtendedPublic(UserGroupReadPublic):
    """Model to extend the User Group public data read from the DB.

    Attributes:
    ----------
        uid (int): User Group unique ID.
        description (str): Brief description.
        name (str): User Group name.
        slas (list of SLARead): Owned SLAs.
    """

    slas: List[SLAReadPublic] = Field(default_factory=list, description=DOC_EXT_SLA)


class IdentityProviderReadExtended(IdentityProviderRead):
    """Model to extend the Identity Provider data read from the DB.

    Attributes:
    ----------
        uid (int): Identity Provider unique ID.
        description (str): Brief description.
        endpoint (str): URL of the Identity Provider.
        group_claim (str): value of the key from which retrieve
            the user group name from an authentication token.
        relationship (AuthMethodRead): Authentication method used by the target
            provider to connect.
        user_groups (list of UserGroupReadExtended): Owned user groups.
    """

    relationship: AuthMethodRead = Field(description=DOC_EXT_AUTH_METH)
    user_groups: List[UserGroupReadExtended] = Field(
        default_factory=list, description=DOC_EXT_GROUP
    )


class IdentityProviderReadExtendedPublic(IdentityProviderReadPublic):
    """Model to extend the Identity Provider public data read from the DB.

    Attributes:
    ----------
        uid (int): Identity Provider unique ID.
        description (str): Brief description.
        endpoint (str): URL of the Identity Provider.
        relationship (AuthMethodRead): Authentication method used by the target
            provider to connect.
        user_groups (list of UserGroupReadExtendedPublic): Owned user groups.
    """

    relationship: AuthMethodRead = Field(description=DOC_EXT_AUTH_METH)
    user_groups: List[UserGroupReadExtendedPublic] = Field(
        default_factory=list, description=DOC_EXT_GROUP
    )


class BlockStorageServiceReadExtended(BlockStorageServiceRead):
    """Model to extend the Block Storage Service data read from the DB.

    Attributes:
    ----------
        uid (int): Service unique ID.
        description (str): Brief description.
        endpoint (str): URL of the IaaS Service.
        type (str): Service type.
        name (str): Service name.
        quotas (list of BlockStorageQuotaReadExtended): Quotas pointing to this service.
    """

    quotas: List[BlockStorageQuotaRead] = Field(
        default_factory=list, description=DOC_EXT_QUOTA
    )


class BlockStorageServiceReadExtendedPublic(BlockStorageServiceReadPublic):
    """Model to extend the Block Storage Service data read from the DB.

    Attributes:
    ----------
        uid (int): Service unique ID.
        description (str): Brief description.
        endpoint (str): URL of the IaaS Service.
        region (RegionReadExtendedPublic): Region hosting this service.
        quotas (list of BlockStorageQuotaReadExtendedPublic): Quotas pointing to this
            service.
    """

    quotas: List[BlockStorageQuotaReadPublic] = Field(
        default_factory=list, description=DOC_EXT_QUOTA
    )


class ComputeServiceReadExtended(ComputeServiceRead):
    """Model to extend the Compute Service data read from the DB.

    Attributes:
    ----------
        uid (int): Service unique ID.
        description (str): Brief description.
        endpoint (str): URL of the IaaS Service.
        type (str): Service type.
        name (str): Service name.
        flavors (list of FlavorRead): Supplied flavors.
        images (list of ImageRead): Supplied images.
        quotas (list of ComputeQuotaReadExtended): Quotas pointing to this service.
    """

    flavors: List[FlavorRead] = Field(default_factory=list, description=DOC_EXT_FLAV)
    images: List[ImageRead] = Field(default_factory=list, description=DOC_EXT_IMAG)
    quotas: List[ComputeQuotaRead] = Field(
        default_factory=list, description=DOC_EXT_QUOTA
    )


class ComputeServiceReadExtendedPublic(ComputeServiceReadPublic):
    """Model to extend the Compute Service public data read from the DB.

    Attributes:
    ----------
        uid (int): Service unique ID.
        description (str): Brief description.
        endpoint (str): URL of the IaaS Service.
        flavors (list of FlavorReadPublic): Supplied flavors.
        images (list of ImageReadPublic): Supplied images.
        quotas (list of ComputeQuotaReadExtendedPublic): Quotas pointing to this
            service.
    """

    flavors: List[FlavorReadPublic] = Field(
        default_factory=list, description=DOC_EXT_FLAV
    )
    images: List[ImageReadPublic] = Field(
        default_factory=list, description=DOC_EXT_IMAG
    )
    quotas: List[ComputeQuotaReadPublic] = Field(
        default_factory=list, description=DOC_EXT_QUOTA
    )


class NetworkServiceReadExtended(NetworkServiceRead):
    """Model to extend the Network Service data read from the DB.

    Attributes:
    ----------
        uid (int): Service unique ID.
        description (str): Brief description.
        endpoint (str): URL of the IaaS Service.
        type (str): Service type.
        name (str): Service name.
        networks (list of NetworkRead): Supplied networks.
        quotas (list of NetworkQuotaReadExtended): Quotas pointing to this
            service.
    """

    networks: List[NetworkRead] = Field(default_factory=list, description=DOC_EXT_NETW)
    quotas: List[NetworkQuotaRead] = Field(
        default_factory=list, description=DOC_EXT_QUOTA
    )


class NetworkServiceReadExtendedPublic(NetworkServiceReadPublic):
    """Model to extend the Network Service public data read from the DB.

    Attributes:
    ----------
        uid (int): Service unique ID.
        description (str): Brief description.
        endpoint (str): URL of the IaaS Service.
        networks (list of NetworkReadPublic): Supplied networks.
        quotas (list of NetworkQuotaReadExtendedPublic): Quotas pointing to this
            service.
    """

    networks: List[NetworkReadPublic] = Field(
        default_factory=list, description=DOC_EXT_NETW
    )
    quotas: List[NetworkQuotaReadPublic] = Field(
        default_factory=list, description=DOC_EXT_QUOTA
    )


class RegionReadExtended(RegionRead):
    """Model to extend the Region data read from the DB.

    Attributes:
    ----------
        uid (uuid): AssociatedRegion unique ID.
        description (str): Brief description.
        name (str): Name of the Region in the Provider.
        location (LocationRead | None): Location hosting this region.
        services (list of Service): Supplied services (block-storage, compute, identity
            and network type).
    """

    location: Optional[LocationRead] = Field(default=None, description=DOC_EXT_LOC)
    services: List[
        Union[
            BlockStorageServiceReadExtended,
            ComputeServiceReadExtended,
            IdentityServiceRead,
            NetworkServiceReadExtended,
        ]
    ] = Field(default_factory=list, description=DOC_EXT_SERV)


class RegionReadExtendedPublic(RegionReadPublic):
    """Model to extend the Region public data read from the DB.

    Attributes:
    ----------
        uid (uuid): AssociatedRegion unique ID.
        description (str): Brief description.
        name (str): Name of the Region in the Provider.
        location (LocationReadPublic | None): Location hosting this region.
        services (list of ServicePublic): Supplied services (block-storage, compute,
            identity and network type).
    """

    location: Optional[LocationReadPublic] = Field(
        default=None, description=DOC_EXT_LOC
    )
    services: List[
        Union[
            BlockStorageServiceReadExtendedPublic,
            ComputeServiceReadExtendedPublic,
            IdentityServiceReadPublic,
            NetworkServiceReadExtendedPublic,
        ]
    ] = Field(default_factory=list, description=DOC_EXT_SERV)


class ProviderReadExtended(ProviderRead):
    """Model to extend the Provider data read from the DB.

    Attributes:
    ----------
        uid (int): Provider unique ID.
        description (str): Brief description.
        name (str): Provider name.
        type (str): Provider type.
        status (str | None): Provider status.
        is_public (bool): Public or private Provider.
        support_email (list of str): List of maintainers emails.
        identity_providers (list of IdentityProviderReadExtended): Supported identity
            providers.
        projects (list of ProjectRead): Supplied projects.
        regions (list of RegionReadExtended): Supplied regions.
    """

    identity_providers: List[IdentityProviderReadExtended] = Field(
        description=DOC_EXT_IDP
    )
    projects: List[ProjectRead] = Field(description=DOC_EXT_PROJ)
    regions: List[RegionReadExtended] = Field(description=DOC_EXT_REG)


class ProviderReadExtendedPublic(ProviderReadPublic):
    """Model to extend the Provider public data read from the DB.

    Attributes:
    ----------
        uid (int): Provider unique ID.
        description (str): Brief description.
        name (str): Provider name.
        identity_providers (list of IdentityProviderReadExtendedPublic): Supported
            identity providers.
        projects (list of ProjectReadPublic): Supplied projects.
        projects (list of RegionReadExtendedPublic): Supplied regions.
    """

    identity_providers: List[IdentityProviderReadExtendedPublic] = Field(
        description=DOC_EXT_IDP
    )
    projects: List[ProjectRead] = Field(description=DOC_EXT_PROJ)
    regions: List[RegionReadExtendedPublic] = Field(description=DOC_EXT_REG)


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
    """Model to extend the SLA data to add to the DB.

    Attributes:
    ----------
        description (str): Brief description.
        doc_uuid (str): Unique ID of the document with the SLA details.
        start_date (datetime): SLA validity start date.
        end_date (datetime): SLA validity end date.
        project (str): Target project's UUID in the Provider.
    """

    project: str = Field(description=DOC_NEW_PROJ_UUID)


class UserGroupCreateExtended(UserGroupCreate):
    """Model to extend the User Group data to add to the DB.

    Attributes:
    ----------
        description (str): Brief description.
        name (str): User Group name in the Identity Provider.
        sla (SLACreateExtended): SLA owned by this project and related to this provider.
    """

    sla: SLACreateExtended = Field(description="SLA related to this provider")


class IdentityProviderCreateExtended(IdentityProviderCreate):
    """Model to extend the Identity Provider data to add to the DB.

    Attributes:
    ----------
        description (str): Brief description.
        endpoint (str): URL of the Identity Provider.
        group_claim (str): Value of the key from which retrieve the user group name from
            an authentication token.
        relationship (AuthMethodCreate): Authentication method used to connect to the
            target identity provider.
        user_groups (list of UserGroupCreateExtended): Owned user groups.
    """

    relationship: AuthMethodCreate = Field(description=DOC_EXT_AUTH_METH)
    user_groups: List[UserGroupCreateExtended] = Field(description=DOC_NEW_GROUP)

    @validator("user_groups")
    @classmethod
    def validate_user_groups(
        cls, v: List[UserGroupCreateExtended]
    ) -> List[UserGroupCreateExtended]:
        """Verify the list is not empty and there are no duplicates."""
        find_duplicates(v, "name")
        assert len(v), "Identity provider's user group list can't be empty"
        return v


class BlockStorageQuotaCreateExtended(BlockStorageQuotaCreate):
    """Model to extend the Block Storage Quota data to add to the DB.

    Attributes:
    ----------
        description (str): Brief description.
        type (str): Quota type.
        per_user (str): This limitation should be applied to each user.
        gigabytes (int | None): Number of max usable gigabytes (GiB).
        per_volume_gigabytes (int | None): Number of max usable gigabytes per volume
            (GiB).
        volumes (int | None): Number of max volumes a user group can create.
        project (str): Target project's UUID in the Provider.
    """

    project: str = Field(description=DOC_NEW_PROJ_UUID)


class ComputeQuotaCreateExtended(ComputeQuotaCreate):
    """Model to extend the Compute Quota data to add to the DB.

    Attributes:
    ----------
        description (str): Brief description.
        type (str): Quota type.
        per_user (str): This limitation should be applied to each user.
        cores (int | None): Number of max usable cores.
        instances (int | None): Number of max VM instances.
        ram (int | None): Number of max usable RAM (MiB).
        project (str): Target project's UUID in the Provider.
    """

    project: str = Field(description=DOC_NEW_PROJ_UUID)


class NetworkQuotaCreateExtended(NetworkQuotaCreate):
    """Model to extend the Network Quota data to add to the DB.

    Attributes:
    ----------
        description (str): Brief description.
        type (str): Quota type.
        per_user (str): This limitation should be applied to each user.
        public_ips (int | None): The number of floating IP addresses allowed for each
            project.
        networks (int | None): The number of networks allowed for each project.
        port (int | None): The number of ports allowed for each project.
        security_groups (int | None): The number of security groups allowed for each
            project.
        security_group_rules (int | None): The number of security group rules allowed
            for each project.
        project (str): Target project's UUID in the Provider.
    """

    project: str = Field(description=DOC_NEW_PROJ_UUID)


class FlavorCreateExtended(FlavorCreate):
    """Model to extend the Flavor data to add to the DB.

    Attributes:
    ----------
        description (str): Brief description.
        name (str): Flavor name in the Provider.
        uuid (str): Flavor unique ID in the Provider
        disk (int): Reserved disk size (GiB)
        is_public (bool): Public or private Flavor.
        ram (int): Reserved RAM (MiB)
        vcpus (int): Number of Virtual CPUs.
        swap (int): Swap size (GiB).
        ephemeral (int): Ephemeral disk size (GiB).
        infiniband (bool): MPI - parallel multi-process enabled.
        gpus (int): Number of GPUs.
        gpu_model (str | None): GPU model name.
        gpu_vendor (str | None): Name of the GPU vendor.
        local_storage (str | None): Local storage presence.
        projects (list of str): List of project' UUIDs in the Provider having access to
            the resource.
    """

    projects: List[str] = Field(default_factory=list, description=DOC_NEW_PROJ_UUIDS)

    @validator("projects")
    @classmethod
    def validate_projects(cls, v: List[str]) -> List[str]:
        """Cast to string possible UUIDs and verify there are no duplicate values."""
        find_duplicates(v)
        return v

    @root_validator
    def project_require_if_private_flavor(
        cls, values: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Verify list emptiness based on flavor type.

        If public verify the projects list is empty, otherwise the list can't be empty.
        """
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
    """Model to extend the Image data to add to the DB.

    Attributes:
    ----------
        description (str): Brief description.
        name (str): Image name in the Provider.
        uuid (str): Image unique ID in the Provider
        os_type (str | None): OS type.
        os_distro (str | None): OS distribution.
        os_version (str | None): Distribution version.
        architecture (str | None): OS architecture.
        kernel_id (str | None): Kernel version.
        cuda_support (str): Support for cuda enabled.
        gpu_driver (str): Support for GPUs drivers.
        is_public (bool): Public or private Image.
        tags (list of str): List of tags associated to this Image.
        projects (list of str): List of project' UUIDs in the Provider having access to
            the resource.
    """

    projects: List[str] = Field(default_factory=list, description=DOC_NEW_PROJ_UUIDS)

    @validator("projects")
    @classmethod
    def validate_projects(cls, v: List[str]) -> str:
        """Cast to string possible UUIDs and verify there are no duplicate values."""
        find_duplicates(v)
        return v

    @root_validator
    def project_require_if_private_image(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Verify list emptiness based on image type.

        If public verify the projects list is empty, otherwise the list can't be empty.
        """
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
    """Model to extend the Network data to add to the DB.

    Attributes:
    ----------
        description (str): Brief description.
        name (str): Network name in the Provider.
        uuid (str): Network unique ID in the Provider
        is_shared (bool): Public or private Network.
        is_router_external (bool): Network with access to outside networks. Externa
            network.
        is_default (bool): Network to use as default.
        mtu (int | None): Metric transmission unit (B).
        proxy_ip (str | None): Proxy IP address.
        proxy_user (str | None): Proxy username.
        tags (list of str): List of tags associated to this Network.
        project (str | None): Target project's UUID in the Provider.
    """

    project: Optional[str] = Field(default=None, description=DOC_NEW_PROJ_UUID)

    @root_validator
    def project_require_if_private_net(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Verify target project is defined based on network type.

        If shared verify the project is None, otherwise the project must be defined.
        """
        if not values.get("is_shared"):
            assert values.get("project") is not None
        else:
            assert not values.get("project")
        return values


class BlockStorageServiceCreateExtended(BlockStorageServiceCreate):
    """Model to extend the Block Storage Service data to add to the DB.

    Attributes:
    ----------
        description (str): Brief description.
        endpoint (str): URL of the IaaS Service.
        type (str): Service type.
        name (str): Service name. Depends on type.
        quotas (list of BlockStorageQuotaCreateExtended): Quotas pointing to this
            service.
    """

    quotas: List[BlockStorageQuotaCreateExtended] = Field(
        default_factory=list, description=DOC_EXT_QUOTA
    )

    @validator("quotas")
    @classmethod
    def max_two_quotas_on_same_project(
        cls, v: List[BlockStorageQuotaCreateExtended]
    ) -> List[BlockStorageQuotaCreateExtended]:
        """Verify maximum number of quotas on same project.

        A project can have at most one `project` quota and one `per-user` quota on a
        specific service.
        """
        d = {}
        for quota in v:
            if quota.project is not None:
                msg = f"Multiple quotas on same project {quota.project}"
                q = d.get(quota.project)
                if not q:
                    d[quota.project] = [1, quota.per_user]
                else:
                    q[0] += 1
                    assert q[0] <= 2 and q[1] != quota.per_user, msg
        return v


class ComputeServiceCreateExtended(ComputeServiceCreate):
    """Model to extend the Compute Service data to add to the DB.

    Attributes:
    ----------
        description (str): Brief description.
        endpoint (str): URL of the IaaS Service.
        type (str): Service type.
        name (str): Service name. Depends on type.
        quotas (list of ComputeQuotaCreateExtended): Quotas pointing to this service.
        flavors (list of FlavorRead): Supplied flavors.
        images (list of ImageRead): Supplied images.
    """

    flavors: List[FlavorCreateExtended] = Field(
        default_factory=list, description=DOC_EXT_FLAV
    )
    images: List[ImageCreateExtended] = Field(
        default_factory=list, description=DOC_EXT_IMAG
    )
    quotas: List[ComputeQuotaCreateExtended] = Field(
        default_factory=list, description=DOC_EXT_QUOTA
    )

    @validator("flavors")
    @classmethod
    def validate_flavors(
        cls, v: List[FlavorCreateExtended]
    ) -> List[FlavorCreateExtended]:
        """Verify there are no duplicated names or UUIDs in the flavor list."""
        find_duplicates(v, "uuid")
        find_duplicates(v, "name")
        return v

    @validator("images")
    @classmethod
    def validate_images(cls, v: List[ImageCreateExtended]) -> List[ImageCreateExtended]:
        """Verify there are no duplicated names or UUIDs in the image list."""
        find_duplicates(v, "uuid")
        find_duplicates(v, "name")
        return v

    @validator("quotas")
    @classmethod
    def max_two_quotas_on_same_project(
        cls, v: List[ComputeQuotaCreateExtended]
    ) -> List[ComputeQuotaCreateExtended]:
        """Verify maximum number of quotas on same project.

        A project can have at most one `project` quota and one `per-user` quota on a
        specific service.
        """
        d = {}
        for quota in v:
            if quota.project is not None:
                msg = f"Multiple quotas on same project {quota.project}"
                q = d.get(quota.project)
                if not q:
                    d[quota.project] = [1, quota.per_user]
                else:
                    q[0] += 1
                    assert q[0] <= 2 and q[1] != quota.per_user, msg
        return v


class NetworkServiceCreateExtended(NetworkServiceCreate):
    """Model to extend the Network Service data to add to the DB.

    Attributes:
    ----------
        description (str): Brief description.
        endpoint (str): URL of the IaaS Service.
        type (str): Service type.
        name (str): Service name. Depends on type.
        quotas (list of NetworkQuotaCreateExtended): Quotas pointing to this service.
        networks (list of NetworkRead): Supplied networks.
    """

    networks: List[NetworkCreateExtended] = Field(
        default_factory=list, description=DOC_EXT_NETW
    )
    quotas: List[NetworkQuotaCreateExtended] = Field(
        default_factory=list, description=DOC_EXT_QUOTA
    )

    @validator("networks")
    @classmethod
    def validate_networks(
        cls, v: List[NetworkCreateExtended]
    ) -> List[NetworkCreateExtended]:
        """Verify there are no duplicated UUIDs in the network list."""
        find_duplicates(v, "uuid")
        return v

    @validator("quotas")
    @classmethod
    def max_two_quotas_on_same_project(
        cls, v: List[NetworkQuotaCreateExtended]
    ) -> List[NetworkQuotaCreateExtended]:
        """Verify maximum number of quotas on same project.

        A project can have at most one `project` quota and one `per-user` quota on a
        specific service.
        """
        d = {}
        for quota in v:
            if quota.project is not None:
                msg = f"Multiple quotas on same project {quota.project}"
                q = d.get(quota.project)
                if not q:
                    d[quota.project] = [1, quota.per_user]
                else:
                    q[0] += 1
                    assert q[0] <= 2 and q[1] != quota.per_user, msg
        return v


class RegionCreateExtended(RegionCreate):
    """Model to extend the Region data to add to the DB.

    Attributes:
    ----------
        uid (uuid): AssociatedRegion unique ID.
        description (str): Brief description.
        name (str): Name of the Region in the Provider.
        provider (ProviderRead): Provider hosting this region.
        location (LocationRead | None): Location hosting this region.
        block_storage_services (list of BlockStorageServiceCreateExtended): Supplied
            block storage services.
        compute_services (list of ComputeServiceCreateExtended): Supplied compute
            services.
        identity_services (list of IdentityServiceCreateExtended): Supplied identity
            services.
        network_services (list of NetworkServiceCreateExtended): Supplied network
            services.
    """

    location: Optional[LocationCreate] = Field(default=None, description=DOC_EXT_LOC)
    block_storage_services: List[BlockStorageServiceCreateExtended] = Field(
        default_factory=list, description=DOC_NEW_SERV_BLO_STO
    )
    compute_services: List[ComputeServiceCreateExtended] = Field(
        default_factory=list, description=DOC_NEW_SERV_COMP
    )
    identity_services: List[IdentityServiceCreate] = Field(
        default_factory=list, description=DOC_NEW_SERV_ID
    )
    network_services: List[NetworkServiceCreateExtended] = Field(
        default_factory=list, description=DOC_NEW_SERV_NET
    )

    @validator("block_storage_services")
    @classmethod
    def validate_block_storage_services(
        cls, v: List[BlockStorageServiceCreateExtended]
    ) -> List[BlockStorageServiceCreateExtended]:
        """Verify there are no duplicated endpoints in the service list."""
        find_duplicates(v, "endpoint")
        return v

    @validator("compute_services")
    @classmethod
    def validate_compute_services(
        cls, v: List[ComputeServiceCreateExtended]
    ) -> List[ComputeServiceCreateExtended]:
        """Verify there are no duplicated endpoints in the service list."""
        find_duplicates(v, "endpoint")
        return v

    @validator("identity_services")
    @classmethod
    def validate_identity_services(
        cls, v: List[IdentityServiceCreate]
    ) -> List[IdentityServiceCreate]:
        """Verify there are no duplicated endpoints in the service list."""
        find_duplicates(v, "endpoint")
        return v

    @validator("network_services")
    @classmethod
    def validate_network_services(
        cls, v: List[NetworkServiceCreateExtended]
    ) -> List[NetworkServiceCreateExtended]:
        """Verify there are no duplicated endpoints in the service list."""
        find_duplicates(v, "endpoint")
        return v


class ProviderCreateExtended(ProviderCreate):
    """Model to extend the Provider data to add to the DB.

    Attributes:
    ----------
        description (str): Brief description.
        name (str): Provider name.
        type (str): Provider type.
        status (str | None): Provider status.
        is_public (bool): Public or private Provider.
        support_email (list of str): List of maintainers emails.
        identity_providers (list of IdentityProviderCreateExtended): Supported identity
            providers.
        projects (list of ProjectCreate): Supplied projects.
        regions (list of RegionCreateExtended): Supplied regions.
    """

    identity_providers: List[IdentityProviderCreateExtended] = Field(
        default_factory=list, description=DOC_EXT_IDP
    )
    projects: List[ProjectCreate] = Field(
        default_factory=list, description=DOC_EXT_PROJ
    )
    regions: List[RegionCreateExtended] = Field(
        default_factory=list, description=DOC_EXT_REG
    )

    @validator("identity_providers")
    @classmethod
    def validate_identity_providers(
        cls, v: List[IdentityProviderCreateExtended]
    ) -> List[IdentityProviderCreateExtended]:
        """Verify there are no duplicated endpoints in the identity provider list."""
        find_duplicates(v, "endpoint")
        return v

    @validator("projects")
    @classmethod
    def validate_projects(cls, v: List[ProjectCreate]) -> List[ProjectCreate]:
        """Verify there are no duplicated names and UUIDs in the project list."""
        find_duplicates(v, "uuid")
        find_duplicates(v, "name")
        return v

    @validator("regions")
    @classmethod
    def validate_regions(
        cls, v: List[RegionCreateExtended]
    ) -> List[RegionCreateExtended]:
        """Verify there are no duplicated names in the region list."""
        find_duplicates(v, "name")
        return v

    @root_validator
    def check_idp_projs_exits(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Verify SLA and Projects relations.

        Check that an SLA is not used by multiple user groups.
        Check that the SLA's projects belong to the target provider.
        """
        projects: List[ProjectCreate] = [i.uuid for i in values.get("projects", [])]
        seen = set()
        identity_providers: List[IdentityProviderCreateExtended] = values.get(
            "identity_providers", []
        )
        for identity_provider in identity_providers:
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
        return values

    @root_validator
    def check_block_storage_serv_projs_exist(
        cls, values: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Verify Block Storage Service projects belong to the target provider."""
        projects: List[ProjectCreate] = [i.uuid for i in values.get("projects", [])]
        regions: List[RegionCreateExtended] = values.get("regions", [])
        for region in regions:
            for service in region.block_storage_services:
                for quota in service.quotas:
                    if quota.project is not None:
                        msg = f"Block storage quota's project {quota.project} "
                        msg += f"not in this provider: {projects}"
                        assert quota.project in projects, msg
        return values

    @root_validator
    def check_compute_serv_projs_exist(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Verify Compute Service and Projects relations.

        Check that the Compute Service's projects, flavors and images belong to the
        target provider.
        """
        projects: List[ProjectCreate] = [i.uuid for i in values.get("projects", [])]
        regions: List[RegionCreateExtended] = values.get("regions", [])
        for region in regions:
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
        return values

    @root_validator
    def check_network_serv_projs_exist(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Verify Network Service and Projects relations.

        Check that the Compute Service's projects, networks belong to the target
        provider.
        """
        projects: List[ProjectCreate] = [i.uuid for i in values.get("projects", [])]
        regions: List[RegionCreateExtended] = values.get("regions", [])
        for region in regions:
            for service in region.network_services:
                for network in service.networks:
                    if network.project is not None:
                        msg = f"Network {network.name}'s project {network.project} "
                        msg += f"not in this provider: {projects}"
                        assert network.project in projects, msg
                for quota in service.quotas:
                    if quota.project is not None:
                        msg = f"Network quota's project {quota.project} "
                        msg += f"not in this provider: {projects}"
                        assert quota.project in projects, msg
        return values
