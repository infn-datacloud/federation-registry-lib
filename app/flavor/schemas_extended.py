"""Pydantic extended models of the Virtual Machine Flavor owned by a Provider."""
from typing import List

from pydantic import Field

from app.flavor.schemas import FlavorRead, FlavorReadPublic
from app.project.schemas import ProjectRead, ProjectReadPublic
from app.provider.schemas import ProviderRead, ProviderReadPublic
from app.region.schemas import RegionRead, RegionReadPublic
from app.service.schemas import ComputeServiceRead, ComputeServiceReadPublic


class RegionReadExtended(RegionRead):
    """Model to extend the Region data read from the DB.

    Add the provider hosting this region.
    """

    provider: ProviderRead = Field(description="Provider hosting this region")


class RegionReadExtendedPublic(RegionReadPublic):
    """Model to extend the Region public data read from the DB.

    Add the provider hosting this region.
    """

    provider: ProviderReadPublic = Field(description="Provider hosting this region")


class ComputeServiceReadExtended(ComputeServiceRead):
    """Model to extend the Compute Service data read from the DB.

    Add the region hosting this service.
    """

    region: RegionReadExtended = Field(description="Provider hosting this service")


class ComputeServiceReadExtendedPublic(ComputeServiceReadPublic):
    """Model to extend the Compute Service public data read from the DB.

    Add the region hosting this service.
    """

    region: RegionReadExtendedPublic = Field(
        description="Provider hosting this service"
    )


class FlavorReadExtended(FlavorRead):
    """Model to extend the Flavor data read from the DB.

    Add the lists of related projects and services.
    """

    projects: List[ProjectRead] = Field(
        description="Projects having access to this flavor. "
        "Empty list if the flavor is public"
    )
    services: List[ComputeServiceReadExtended] = Field(
        description="ComputeService owning this Flavor."
    )


class FlavorReadExtendedPublic(FlavorReadPublic):
    """Model to extend the Flavor public data read from the DB.

    Add the lists of related projects and services.
    """

    projects: List[ProjectReadPublic] = Field(
        description="Projects having access to this flavor. "
        "Empty list if the flavor is public"
    )
    services: List[ComputeServiceReadExtendedPublic] = Field(
        description="ComputeService owning this Flavor."
    )
