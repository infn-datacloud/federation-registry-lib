from typing import List

from app.flavor.schemas import FlavorCreate, FlavorRead
from app.image.schemas import ImageCreate, ImageRead
from app.location.schemas import LocationCreate, LocationRead
from app.project.schemas import ProjectCreate
from app.project.schemas_extended import ProjectReadExtended
from app.provider.schemas_extended import (
    AuthMethodCreate,
    IdentityProviderCreateExtended,
    IdentityProviderRead,
    ProviderCreateExtended,
    ProviderReadExtended,
)
from app.quota.schemas import CinderQuotaCreate, NovaQuotaCreate, QuotaCreate, QuotaRead
from app.service.schemas import ServiceCreate, ServiceRead
from pydantic import UUID4, AnyHttpUrl, BaseModel, Field


class URLs(BaseModel):
    flavors: AnyHttpUrl
    identity_providers: AnyHttpUrl
    images: AnyHttpUrl
    locations: AnyHttpUrl
    projects: AnyHttpUrl
    providers: AnyHttpUrl
    quotas: AnyHttpUrl
    services: AnyHttpUrl
    slas: AnyHttpUrl
    user_groups: AnyHttpUrl


class LocationWrite(LocationCreate):
    pass


class AuthMethodWrite(AuthMethodCreate):
    pass


class IdentityProviderWrite(IdentityProviderCreateExtended):
    pass


class QuotaWrite(QuotaCreate):
    pass


class NovaQuotaWrite(NovaQuotaCreate):
    type: str = "org.openstack.nova"


class CinderQuotaWrite(CinderQuotaCreate):
    type: str = "org.openstack.cinder"


class ProjectWrite(ProjectCreate):
    compute_quota: NovaQuotaWrite
    block_storage_quota: CinderQuotaWrite


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
    projects: List[ProjectWrite] = Field(
        default_factory=list, description="List of projects"
    )


class FlavorRead(FlavorRead):
    pass


class IdentityProviderRead(IdentityProviderRead):
    pass


class ImageRead(ImageRead):
    pass


class LocationRead(LocationRead):
    pass


class ProjectRead(ProjectReadExtended):
    pass


class ProviderRead(ProviderReadExtended):
    pass


class ServiceWrite(ServiceCreate):
    pass


class ServiceRead(ServiceRead):
    pass


class QuotaRead(QuotaRead):
    pass
