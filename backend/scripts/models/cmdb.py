from typing import List

from app.flavor.schemas import FlavorCreate, FlavorRead
from app.image.schemas import ImageCreate, ImageRead
from app.project.schemas import ProjectCreate, ProjectRead
from app.provider.schemas_extended import (
    AuthMethodCreate,
    IdentityProviderCreateExtended,
    ProviderCreateExtended,
    ProviderReadExtended,
)
from pydantic import UUID4, AnyHttpUrl, BaseModel, Field


class URLs(BaseModel):
    flavors: AnyHttpUrl
    identity_providers: AnyHttpUrl
    images: AnyHttpUrl
    locations: AnyHttpUrl
    projects: AnyHttpUrl
    providers: AnyHttpUrl
    services: AnyHttpUrl
    slas: AnyHttpUrl
    user_groups: AnyHttpUrl


class AuthMethod(AuthMethodCreate):
    pass


class IdentityProvider(IdentityProviderCreateExtended):
    pass


class Project(ProjectCreate):
    pass


class Flavor(FlavorCreate):
    projects: List[UUID4] = Field(
        default_factory=list,
        description="List of projects UUIDs which have access to this flavor",
    )


class Image(ImageCreate):
    projects: List[UUID4] = Field(
        default_factory=list,
        description="List of projects UUIDs which have access to this image",
    )


class Provider(ProviderCreateExtended):
    flavors: List[Flavor] = Field(default_factory=list, description="List of flavors")
    images: List[Image] = Field(default_factory=list, description="List of images")


class FlavorRead(FlavorRead):
    pass


class ImageRead(ImageRead):
    pass


class ProjectRead(ProjectRead):
    pass


class ProviderRead(ProviderReadExtended):
    pass
