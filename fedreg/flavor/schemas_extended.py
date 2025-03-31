"""Pydantic extended models of the Virtual Machine Flavor owned by a Provider."""

from pydantic import Field

from fedreg.core import BaseReadPrivateExtended, BaseReadPublicExtended
from fedreg.flavor.constants import DOC_EXT_PROJ, DOC_EXT_SERV
from fedreg.flavor.schemas import (
    FlavorRead,
    FlavorReadPublic,
)
from fedreg.project.schemas import ProjectRead, ProjectReadPublic
from fedreg.provider.schemas import ProviderRead, ProviderReadPublic
from fedreg.region.constants import DOC_EXT_PROV
from fedreg.region.schemas import RegionRead, RegionReadPublic
from fedreg.service.constants import DOC_EXT_REG
from fedreg.service.schemas import ComputeServiceRead, ComputeServiceReadPublic


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


class ComputeServiceReadExtended(ComputeServiceRead):
    """Model to extend the Compute Service data read from the DB.

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


class ComputeServiceReadExtendedPublic(ComputeServiceReadPublic):
    """Model to extend the Compute Service public data read from the DB.

    Attributes:
    ----------
        uid (int): Service unique ID.
        description (str): Brief description.
        endpoint (str): URL of the IaaS Service.
        region (RegionReadExtendedPublic): Region hosting this service.
    """

    region: RegionReadExtendedPublic = Field(description=DOC_EXT_REG)


class FlavorReadExtended(BaseReadPrivateExtended, FlavorRead):
    """Model to extend the Flavor data read from the DB.

    Attributes:
    ----------
        uid (str): Flavor unique ID.
        description (str): Brief description.
        name (str): Flavor name in the Resource Provider.
        uuid (str): Flavor unique ID in the Resource Provider.
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
        services (list of ComputeServiceReadExtended):
            Compute Service supporting this flavor.
    """

    projects: list[ProjectRead] = Field(default_factory=list, description=DOC_EXT_PROJ)
    services: list[ComputeServiceReadExtended] = Field(description=DOC_EXT_SERV)


class FlavorReadExtendedPublic(BaseReadPublicExtended, FlavorReadPublic):
    """Model to extend the Flavor public data read from the DB.

    Attributes:
    ----------
        uid (str): Flavor unique ID.
        description (str): Brief description.
        name (str): Flavor name in the Resource Provider.
        uuid (str): Flavor unique ID in the Resource Provider.
        projects (list of ProjectRead):
            Projects having access to this flavor. Filled only for private flavors.
        services (list of ComputeServiceReadExtended):
            Compute Service supporting this flavor.
    """

    projects: list[ProjectReadPublic] = Field(
        default_factory=list, description=DOC_EXT_PROJ
    )
    services: list[ComputeServiceReadExtendedPublic] = Field(description=DOC_EXT_SERV)
