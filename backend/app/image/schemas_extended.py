from pydantic import Field
from typing import List

from app.image.schemas import ImageRead
from app.project.schemas import ProjectRead
from app.provider.schemas import ProviderRead


class ImageReadExtended(ImageRead):
    """Model to extend the Image data read from the
    DB with the lists of related items.
    """

    projects: List[ProjectRead] = Field(
        default_factory=list,
        description="List of projects with access to this Image.",
    )
    provider: ProviderRead = Field(description="Provider owning this Image.")
