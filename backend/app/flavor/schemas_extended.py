from pydantic import Field
from typing import List

from app.flavor.schemas import FlavorRead
from app.project.schemas import ProjectRead
from app.provider.schemas import ProviderRead


class FlavorReadExtended(FlavorRead):
    """Model to extend the Flavor data read from the
    DB with the lists of related items.
    """

    projects: List[ProjectRead] = Field(
        default_factory=list,
        description="List of projects with access to this Flavor.",
    )
    provider: ProviderRead = Field(description="Provider owning this Flavor.")
