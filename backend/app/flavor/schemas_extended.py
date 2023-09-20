from typing import List

from app.flavor.schemas import FlavorRead, FlavorReadPublic
from app.project.schemas import ProjectRead, ProjectReadPublic
from app.provider.schemas import ProviderRead, ProviderReadPublic
from pydantic import Field


class FlavorReadExtended(FlavorRead):
    """Model to extend the Flavor data read from the DB with the lists of
    related items for authenticated users."""

    provider: ProviderRead = Field(description="Provider owning this Flavor.")
    projects: List[ProjectRead] = Field(
        description="Projects having access to this flavor. "
        "Empty list if the flavor is public"
    )


class FlavorReadExtendedPublic(FlavorReadPublic):
    """Model to extend the Flavor data read from the DB with the lists of
    related items for non-authenticated users."""

    provider: ProviderReadPublic = Field(description="Provider owning this Flavor.")
    projects: List[ProjectReadPublic] = Field(
        description="Projects having access to this flavor. "
        "Empty list if the flavor is public"
    )
