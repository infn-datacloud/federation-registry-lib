"""Pydantic extended models of the Virtual Machine StorageClass owned by a Provider."""

from pydantic import Field

from fedreg.core import BaseReadPrivateExtended, BaseReadPublicExtended
from fedreg.project.schemas import ProjectRead, ProjectReadPublic
from fedreg.provider.schemas import ProviderRead, ProviderReadPublic
from fedreg.region.constants import DOC_EXT_PROV
from fedreg.region.schemas import RegionRead, RegionReadPublic
from fedreg.service.constants import DOC_EXT_REG
from fedreg.service.schemas import (
    BlockStorageServiceRead,
    BlockStorageServiceReadPublic,
)
from fedreg.storageclass.schemas import (
    StorageClassRead,
    StorageClassReadPublic,
)


class RegionReadExtended(RegionRead):
    """Model to extend the Region data read from the DB.

    Attributes:
    ----------
        uid (uuid): AssociatedRegion unique ID.
        description (str): Brief description.
        name (str): Name of the Region in the Provider.
        provider (ProviderRead): Provider hosting this region.
    """

    provider: ProviderRead = Field(description=DOC_EXT_PROV)


class RegionReadExtendedPublic(RegionReadPublic):
    """Model to extend the Region public data read from the DB.

    Attributes:
    ----------
        uid (uuid): AssociatedRegion unique ID.
        description (str): Brief description.
        name (str): Name of the Region in the Provider.
        provider (ProviderReadPublic): Provider hosting this region.
    """

    provider: ProviderReadPublic = Field(description=DOC_EXT_PROV)


class BlockStorageServiceReadExtended(BlockStorageServiceRead):
    """Model to extend the BlockStorage Service data read from the DB.

    Attributes:
    ----------
        uid (int): Service unique ID.
        description (str): Brief description.
        endpoint (str): URL of the IaaS Service.
        type (str): Service type.
        name (str): Service name.
        region (RegionReadExtended): Region hosting this service.
    """

    region: RegionReadExtended = Field(description=DOC_EXT_REG)


class BlockStorageServiceReadExtendedPublic(BlockStorageServiceReadPublic):
    """Model to extend the BlockStorage Service public data read from the DB.

    Attributes:
    ----------
        uid (int): Service unique ID.
        description (str): Brief description.
        endpoint (str): URL of the IaaS Service.
        region (RegionReadExtendedPublic): Region hosting this service.
    """

    region: RegionReadExtendedPublic = Field(description=DOC_EXT_REG)


class StorageClassReadExtended(BaseReadPrivateExtended, StorageClassRead):
    """Model to extend the StorageClass data read from the DB.

    Attributes:
    ----------
        uid (str): StorageClass unique ID.
        description (str): Brief description.
        name (str): StorageClass name in the Resource Provider.
        uuid (str): StorageClass unique ID in the Resource Provider.
        disk (int): Reserved disk size (GiB)
        ram (int): Reserved RAM (MiB)
        vcpus (int): Number of Virtual CPUs.
        swap (int): Swap size (GiB).
        ephemeral (int): Ephemeral disk size (GiB).
        infiniband (bool): MPI - parallel multi-process enabled.
        gpus (int): Number of GPUs.
        gpu_model (str | None): GPU model name.
        gpu_vendor (str | None): Name of the GPU vendor.
        local_storage (str | None): Local storage presence.
        is_shared (bool): Public or private Image.
        projects (list of ProjectRead):
            Projects having access to this flavor. Filled only for private flavors.
        services (list of BlockStorageServiceReadExtended):
            BlockStorage Service supporting this flavor.
    """

    projects: list[ProjectRead] = Field(
        default_factory=list,
        description="List of projects allowed to use the storage class.",
    )
    service: BlockStorageServiceReadExtended = Field(
        description="Block Storage service providing the storage class."
    )


class StorageClassReadExtendedPublic(BaseReadPublicExtended, StorageClassReadPublic):
    """Model to extend the StorageClass public data read from the DB.

    Attributes:
    ----------
        uid (str): StorageClass unique ID.
        description (str): Brief description.
        name (str): StorageClass name in the Resource Provider.
        uuid (str): StorageClass unique ID in the Resource Provider.
        projects (list of ProjectRead):
            Projects having access to this flavor. Filled only for private flavors.
        services (list of BlockStorageServiceReadExtended):
            BlockStorage Service supporting this flavor.
    """

    projects: list[ProjectReadPublic] = Field(
        default_factory=list,
        description="List of projects allowed to use the storage class.",
    )
    service: BlockStorageServiceReadExtendedPublic = Field(
        description="Block Storage service providing the storage class."
    )
