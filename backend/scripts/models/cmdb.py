import sys
from pathlib import Path
from typing import List

from pydantic import UUID4, Field

external_path = Path.cwd().parent
sys.path.insert(1, str(external_path))

from app.flavor.schemas import FlavorCreate
from app.image.schemas import ImageCreate
from app.project.schemas import ProjectCreate
from app.provider.schemas_extended import (
    AuthMethodCreate,
    IdentityProviderCreateExtended,
    ProviderCreateExtended,
)


class AuthMethod(AuthMethodCreate):
    pass


class IdentityProvider(IdentityProviderCreateExtended):
    pass


class Project(ProjectCreate):
    pass


class Flavor(FlavorCreate):
    projects: List[UUID4] = Field(default_factory=list)


class Image(ImageCreate):
    projects: List[UUID4] = Field(default_factory=list)


class Provider(ProviderCreateExtended):
    flavors: List[Flavor] = Field(default_factory=list)
    images: List[Image] = Field(default_factory=list)
