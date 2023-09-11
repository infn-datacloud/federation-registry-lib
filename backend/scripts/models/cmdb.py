from typing import List

from app.flavor.schemas import FlavorCreate, FlavorRead
from app.image.schemas import ImageCreate, ImageRead
from app.location.schemas import LocationCreate, LocationRead
from app.project.schemas import ProjectCreate, ProjectRead
from app.provider.schemas_extended import (
    AuthMethodCreate,
    IdentityProviderCreateExtended,
    IdentityProviderRead,
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


class LocationWrite(LocationCreate):
    pass


class AuthMethodWrite(AuthMethodCreate):
    pass


class IdentityProviderWrite(IdentityProviderCreateExtended):
    pass


class ProjectWrite(ProjectCreate):
    pass


class FlavorWrite(FlavorCreate):
    projects: List[UUID4] = Field(
        default_factory=list,
        description="List of projects UUIDs which have access to this flavor",
    )


class ImageWrite(ImageCreate):
    projects: List[UUID4] = Field(
        default_factory=list,
        description="List of projects UUIDs which have access to this image",
    )


class ProviderWrite(ProviderCreateExtended):
    flavors: List[FlavorWrite] = Field(
        default_factory=list, description="List of flavors"
    )
    images: List[ImageWrite] = Field(default_factory=list, description="List of images")


class FlavorRead(FlavorRead):
    pass


class IdentityProviderRead(IdentityProviderRead):
    pass


class ImageRead(ImageRead):
    pass


class LocationRead(LocationRead):
    pass


class ProjectRead(ProjectRead):
    pass


class ProviderRead(ProviderReadExtended):
    pass
