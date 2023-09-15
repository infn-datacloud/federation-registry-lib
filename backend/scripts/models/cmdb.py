from typing import List, Optional

from app.flavor.schemas import FlavorCreate, FlavorQuery, FlavorRead
from app.identity_provider.schemas import IdentityProviderQuery
from app.image.schemas import ImageCreate, ImageQuery, ImageRead
from app.location.schemas import LocationCreate, LocationQuery, LocationRead
from app.project.schemas import ProjectCreate, ProjectQuery
from app.project.schemas_extended import ProjectReadExtended
from app.provider.schemas import ProviderQuery
from app.provider.schemas_extended import (
    AuthMethodCreate,
    IdentityProviderCreateExtended,
    IdentityProviderRead,
    ProviderCreateExtended,
    ProviderReadExtended,
)
from app.quota.schemas import (
    CinderQuotaCreate,
    NovaQuotaCreate,
    QuotaCreate,
    QuotaQuery,
    QuotaRead,
)
from app.service.schemas import ServiceCreate, ServiceQuery, ServiceRead
from pydantic import UUID4, Field


class AuthMethodWrite(AuthMethodCreate):
    pass


class FlavorWrite(FlavorCreate):
    projects: List[UUID4] = Field(
        default_factory=list,
        description="List of projects UUIDs which have access to this flavor",
    )

    def __str__(self) -> str:
        return f"{self.__class__.__name__.replace('Write', '')}={self.name}"


class IdentityProviderWrite(IdentityProviderCreateExtended):
    def __str__(self) -> str:
        return f"{self.__class__.__name__.replace('Write', '')}={self.endpoint}"


class ImageWrite(ImageCreate):
    projects: List[UUID4] = Field(
        default_factory=list,
        description="List of projects UUIDs which have access to this image",
    )

    def __str__(self) -> str:
        return f"{self.__class__.__name__.replace('Write', '')}={self.name}"


class LocationWrite(LocationCreate):
    def __str__(self) -> str:
        return f"{self.__class__.__name__.replace('Write', '')}={self.name}"


class QuotaWrite(QuotaCreate):
    def __str__(self) -> str:
        return f"{self.__class__.__name__.replace('Write', '')}={self.type}"


class NovaQuotaWrite(NovaQuotaCreate):
    type: str = "org.openstack.nova"
    service: Optional[UUID4] = Field(default=None, description="")

    def __str__(self) -> str:
        return f"{self.__class__.__name__.replace('Write', '')}={self.type}"


class CinderQuotaWrite(CinderQuotaCreate):
    type: str = "org.openstack.cinder"
    service: Optional[UUID4] = Field(default=None, description="")

    def __str__(self) -> str:
        return f"{self.__class__.__name__.replace('Write', '')}={self.type}"


class ProjectWrite(ProjectCreate):
    compute_quota: NovaQuotaWrite
    block_storage_quota: CinderQuotaWrite

    def __str__(self) -> str:
        return f"{self.__class__.__name__.replace('Write', '')}={self.name}"


class ServiceWrite(ServiceCreate):
    def __str__(self) -> str:
        return f"{self.__class__.__name__.replace('Write', '')}={self.endpoint}"


class ProviderWrite(ProviderCreateExtended):
    flavors: List[FlavorWrite] = Field(
        default_factory=list, description="List of flavors"
    )
    images: List[ImageWrite] = Field(default_factory=list, description="List of images")
    projects: List[ProjectWrite] = Field(
        default_factory=list, description="List of projects"
    )
    services: List[ServiceWrite] = Field(
        default_factory=list, description="List of services"
    )

    def __str__(self) -> str:
        return f"{self.__class__.__name__.replace('Write', '')}={self.name}"


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


class ServiceRead(ServiceRead):
    pass


class QuotaRead(QuotaRead):
    pass


class FlavorQuery(FlavorQuery):
    pass


class IdentityProviderQuery(IdentityProviderQuery):
    pass


class ImageQuery(ImageQuery):
    pass


class LocationQuery(LocationQuery):
    pass


class ProjectQuery(ProjectQuery):
    pass


class ProviderQuery(ProviderQuery):
    pass


class ServiceQuery(ServiceQuery):
    pass


class QuotaQuery(QuotaQuery):
    pass
