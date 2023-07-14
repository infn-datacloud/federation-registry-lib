from pydantic import Field
from typing import List, Optional

from .schemas import ProviderCreate, ProviderRead, ProviderUpdate
from ..flavor.schemas import FlavorCreate, FlavorRead, FlavorUpdate
from ..identity_provider.schemas_extended import (
    IdentityProviderCreateExtended,
    IdentityProviderReadExtended,
    IdentityProviderUpdateExtended,
)
from ..image.schemas import ImageCreate, ImageRead, ImageUpdate
from ..location.schemas import LocationCreate, LocationRead, LocationUpdate
from ..project.schemas import ProjectCreate, ProjectRead, ProjectUpdate
from ..service.schemas import ServiceCreate, ServiceRead


class ProviderCreateExtended(ProviderCreate):
    """Provider Create Model class.

    Class without id (which is populated by the database).
    Expected as input when performing a PUT or POST request.

    Attributes:
        description (str): Brief description.
        name (str | None): Provider name (type).
        is_public (bool | None): Public or private provider.
        support_email (list of str | None): List of maintainers emails.
        location (LocationCreate | None): provider physical location
        clusters TODO
        flavors TODO
        identity_providers TODO
        images TODO
        projects TODO
        services TODO
    """

    location: Optional[LocationCreate] = None
    flavors: List[FlavorCreate] = Field(default_factory=list)
    identity_providers: List[IdentityProviderCreateExtended] = Field(
        default_factory=list
    )
    images: List[ImageCreate] = Field(default_factory=list)
    projects: List[ProjectCreate] = Field(default_factory=list)
    services: List[ServiceCreate] = Field(default_factory=list)


class ProviderUpdateExtended(ProviderUpdate):
    """Provider Update Model class.

    Class without id (which is populated by the database).
    Expected as input when performing a PATCH request.

    Attributes:
        description (str | None): Brief description.
        name (str | None): Provider name (type).
        is_public (bool | None): Public or private provider.
        support_email (list of str | None): List of maintainers emails.
        location (LocationUpdate | None): provider physical location
        clusters TODO
        flavors TODO
        identity_providers TODO
        images TODO
        projects TODO
        services TODO
    """

    location: Optional[LocationUpdate] = None
    flavors: List[FlavorUpdate] = Field(default_factory=list)
    identity_providers: List[IdentityProviderUpdateExtended] = Field(
        default_factory=list
    )
    images: List[ImageUpdate] = Field(default_factory=list)
    projects: List[ProjectUpdate] = Field(default_factory=list)
    # services: List[ServiceUpdate] = Field(default_factory=list)


class ProviderExtended(ProviderRead):
    """Provider class.

    Class retrieved from the database.
    Expected as output when performing a REST request.
    It contains all the non-sensible data written
    in the database.

    Attributes:
        uid (uuid): Unique ID.
        description (str): Brief description.
        name (str | None): Provider name (type).
        is_public (bool | None): Public or private provider.
        support_email (list of str | None): List of maintainers emails.
        location (LocationCreate | None): provider physical location
        clusters TODO
        flavors TODO
        identity_providers TODO
        images TODO
        projects TODO
        services TODO
    """

    location: Optional[LocationRead] = None
    flavors: List[FlavorRead] = Field(default_factory=list)
    identity_providers: List[IdentityProviderReadExtended] = Field(
        default_factory=list
    )
    images: List[ImageRead] = Field(default_factory=list)
    projects: List[ProjectRead] = Field(default_factory=list)
    services: List[ServiceRead] = Field(default_factory=list)
