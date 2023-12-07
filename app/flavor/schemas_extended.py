"""Pydantic extended models of the Virtual Machine Flavor owned by a Provider."""
from typing import List

from pydantic import Field

from app.flavor.constants import DOC_EXT_PROJ, DOC_EXT_SERV
from app.flavor.schemas import FlavorRead, FlavorReadPublic
from app.project.schemas import ProjectRead, ProjectReadPublic
from app.provider.schemas import ProviderRead, ProviderReadPublic
from app.region.constants import DOC_EXT_PROV
from app.region.schemas import RegionRead, RegionReadPublic
from app.service.constants import DOC_EXT_REG
from app.service.schemas import ComputeServiceRead, ComputeServiceReadPublic


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


class FlavorReadExtended(FlavorRead):
    """Model to extend the Flavor data read from the DB.

    Attributes:
    ----------
        uid (str): Flavor unique ID.
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
        projects (list of ProjectRead): Projects having access to this flavor. The list
            is populated only if the flavor is a private one.
        services (list of ComputeServiceReadExtended): Compute Services exploiting this
            flavor.
    """

    projects: List[ProjectRead] = Field(description=DOC_EXT_PROJ)
    services: List[ComputeServiceReadExtended] = Field(description=DOC_EXT_SERV)


class FlavorReadExtendedPublic(FlavorReadPublic):
    """Model to extend the Flavor public data read from the DB.

    Attributes:
    ----------
        uid (str): Flavor unique ID.
        description (str): Brief description.
        name (str): Flavor name in the Provider.
        uuid (str): Flavor unique ID in the Provider
        projects (list of ProjectReadPublic): Projects having access to this flavor. The
            list is populated only if the flavor is a private one.
        services (list of ComputeServiceReadExtendedPublic): Compute Services exploiting
            this flavor.
    """

    projects: List[ProjectReadPublic] = Field(description=DOC_EXT_PROJ)
    services: List[ComputeServiceReadExtendedPublic] = Field(description=DOC_EXT_SERV)
