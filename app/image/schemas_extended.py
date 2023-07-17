from pydantic import Field
from typing import List

from app.image.schemas import ImageRead
from app.project.schemas import ProjectRead
from app.provider.schemas import ProviderRead


class ImageReadExtended(ImageRead):
    projects: List[ProjectRead] = Field(default_factory=list)
    provider: ProviderRead
