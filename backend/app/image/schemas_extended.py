from typing import List

from app.image.schemas import ImageRead, ImageReadPublic
from app.project.schemas import ProjectRead, ProjectReadPublic
from app.provider.schemas import ProviderRead, ProviderReadPublic
from app.region.schemas import RegionRead, RegionReadPublic
from app.service.schemas import ComputeServiceRead, ComputeServiceReadPublic
from pydantic import Field


class RegionReadExtended(RegionRead):
    provider: ProviderRead = Field(description="Provider hosting this region")


class RegionReadExtendedPublic(RegionReadPublic):
    provider: ProviderReadPublic = Field(description="Provider hosting this region")


class ComputeServiceReadExtended(ComputeServiceRead):
    region: RegionReadExtended = Field(description="Provider hosting this service")


class ComputeServiceReadExtendedPublic(ComputeServiceReadPublic):
    region: RegionReadExtendedPublic = Field(
        description="Provider hosting this service"
    )


class ImageReadExtended(ImageRead):
    """Model to extend the Image data read from the DB with the lists of
    related items for authenticated users."""

    projects: List[ProjectRead] = Field(
        description="Projects having access to this flavor. "
        "Empty list if the flavor is public"
    )
    services: List[ComputeServiceReadExtended] = Field(
        default_factory=list, description="ComputeService owning this Image."
    )


class ImageReadExtendedPublic(ImageReadPublic):
    """Model to extend the Image data read from the DB with the lists of
    related items for non-authenticated users."""

    projects: List[ProjectReadPublic] = Field(
        description="Projects having access to this flavor. "
        "Empty list if the flavor is public"
    )
    services: List[ComputeServiceReadExtendedPublic] = Field(
        default_factory=list, description="ComputeService owning this Image."
    )
