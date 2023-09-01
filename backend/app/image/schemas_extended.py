from typing import List

from app.image.schemas import ImageRead, ImageReadPublic
from app.project.schemas import ProjectRead, ProjectReadPublic
from app.provider.schemas import ProviderRead, ProviderReadPublic
from pydantic import Field


class ImageReadExtended(ImageRead):
    """Model to extend the Image data read from the DB with the lists of
    related items for authenticated users."""

    projects: List[ProjectRead] = Field(
        default_factory=list,
        description="List of projects with access to this Image.",
    )
    provider: ProviderRead = Field(description="Provider owning this Image.")


class ImageReadExtendedPublic(ImageReadPublic):
    """Model to extend the Image data read from the DB with the lists of
    related items for non-authenticated users."""

    projects: List[ProjectReadPublic] = Field(
        default_factory=list,
        description="List of projects with access to this Image.",
    )
    provider: ProviderReadPublic = Field(description="Provider owning this Image.")
