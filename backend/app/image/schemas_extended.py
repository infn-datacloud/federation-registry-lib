from typing import List

from app.image.schemas import ImageRead, ImageReadPublic
from app.project.schemas import ProjectRead, ProjectReadPublic
from app.service.schemas import ComputeServiceRead, ComputeServiceReadPublic
from pydantic import Field


class ImageReadExtended(ImageRead):
    """Model to extend the Image data read from the DB with the lists of
    related items for authenticated users."""

    service: ComputeServiceRead = Field(description="ComputeService owning this Image.")
    projects: List[ProjectRead] = Field(
        description="Projects having access to this flavor. "
        "Empty list if the flavor is public"
    )


class ImageReadExtendedPublic(ImageReadPublic):
    """Model to extend the Image data read from the DB with the lists of
    related items for non-authenticated users."""

    service: ComputeServiceReadPublic = Field(
        description="ComputeService owning this Image."
    )
    projects: List[ProjectReadPublic] = Field(
        description="Projects having access to this flavor. "
        "Empty list if the flavor is public"
    )
