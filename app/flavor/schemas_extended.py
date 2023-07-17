from pydantic import Field
from typing import List

from app.flavor.schemas import FlavorRead
from app.project.schemas import ProjectRead
from app.provider.schemas import ProviderRead


class FlavorReadExtended(FlavorRead):
    projects: List[ProjectRead] = Field(default_factory=list)
    provider: ProviderRead
