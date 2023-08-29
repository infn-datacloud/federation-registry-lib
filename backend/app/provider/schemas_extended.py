from typing import List, Optional, Union

from app.auth_method.schemas import AuthMethodCreate, AuthMethodRead
from app.flavor.schemas import FlavorCreate, FlavorRead
from app.identity_provider.schemas import IdentityProviderCreate, IdentityProviderRead
from app.image.schemas import ImageCreate, ImageRead
from app.location.schemas import LocationCreate, LocationRead
from app.project.schemas import ProjectCreate, ProjectRead
from app.provider.schemas import ProviderCreate, ProviderRead
from app.service.schemas import (
    ChronosServiceCreate,
    ChronosServiceRead,
    KubernetesServiceCreate,
    KubernetesServiceRead,
    MarathonServiceCreate,
    MarathonServiceRead,
    MesosServiceCreate,
    MesosServiceRead,
    NovaServiceCreate,
    NovaServiceRead,
    OneDataServiceCreate,
    OneDataServiceRead,
    RucioServiceCreate,
    RucioServiceRead,
)
from pydantic import Field


class IdentityProviderCreateExtended(IdentityProviderCreate):
    """Model to extend the Identity Provider data used to create a new instance
    in the DB with the authentication method details."""

    relationship: AuthMethodCreate = Field(
        description="Authentication method used by the Provider"
    )


class IdentityProviderReadExtended(IdentityProviderRead):
    """Model to extend the Identity Provider data read from the DB with the
    authentication method details."""

    relationship: AuthMethodRead = Field(
        description="Authentication method used by the Provider"
    )


class ProviderCreateExtended(ProviderCreate):
    """Model to extend the Provider data used to create a new instance in the
    DB with the lists of related items."""

    location: Optional[LocationCreate] = Field(
        default=None, description="Provider location."
    )
    flavors: List[FlavorCreate] = Field(
        default_factory=list, description="List of owned Flavors."
    )
    identity_providers: List[IdentityProviderCreateExtended] = Field(
        default_factory=list,
        description="List of supported identity providers.",
    )
    images: List[ImageCreate] = Field(
        default_factory=list, description="List of owned Images."
    )
    projects: List[ProjectCreate] = Field(
        default_factory=list, description="List of owned Projects."
    )
    services: List[
        Union[
            ChronosServiceCreate,
            KubernetesServiceCreate,
            MarathonServiceCreate,
            MesosServiceCreate,
            NovaServiceCreate,
            OneDataServiceCreate,
            RucioServiceCreate,
        ]
    ] = Field(default_factory=list, description="List of hosted Services.")


class ProviderReadExtended(ProviderRead):
    """Model to extend the Provider data read from the DB with the lists of
    related items."""

    location: Optional[LocationRead] = Field(
        default=None, description="Provider location."
    )
    flavors: List[FlavorRead] = Field(
        default_factory=list, description="List of owned Flavors."
    )
    identity_providers: List[IdentityProviderReadExtended] = Field(
        default_factory=list,
        description="List of supported identity providers.",
    )
    images: List[ImageRead] = Field(
        default_factory=list, description="List of owned Images."
    )
    projects: List[ProjectRead] = Field(
        default_factory=list, description="List of owned Projects."
    )
    services: List[
        Union[
            ChronosServiceRead,
            KubernetesServiceRead,
            MarathonServiceRead,
            MesosServiceRead,
            NovaServiceRead,
            OneDataServiceRead,
            RucioServiceRead,
        ]
    ] = Field(default_factory=list, description="List of hosted Services.")
