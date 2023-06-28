from pydantic import Field
from typing import List, Optional

from .schemas import Provider, ProviderCreate, ProviderUpdate
from ..cluster.schemas_extended import (
    ClusterExtended,
    ClusterCreateExtended,
    ClusterUpdateExtended,
)
from ..flavor.schemas_extended import (
    FlavorExtended,
    FlavorCreateExtended,
    FlavorUpdateExtended,
)
from ..identity_provider.schemas_extended import (
    IdentityProviderExtended,
    IdentityProviderCreateExtended,
    IdentityProviderUpdateExtended,
)
from ..image.schemas_extended import (
    ImageExtended,
    ImageCreateExtended,
    ImageUpdateExtended,
)
from ..location.schemas import Location, LocationCreate, LocationUpdate
from ..project.schemas_extended import (
    ProjectExtended,
    ProjectCreateExtended,
    ProjectUpdateExtended,
)
from ..service.schemas_extended import (
    ServiceExtended,
    ServiceCreateExtended,
    ServiceUpdateExtended,
)


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
    clusters: List[ClusterCreateExtended] = Field(default_factory=list)
    flavors: List[FlavorCreateExtended] = Field(default_factory=list)
    identity_providers: List[IdentityProviderCreateExtended] = Field(
        default_factory=list
    )
    images: List[ImageCreateExtended] = Field(default_factory=list)
    projects: List[ProjectCreateExtended] = Field(default_factory=list)
    services: List[ServiceCreateExtended] = Field(default_factory=list)


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
    clusters: List[ClusterUpdateExtended] = Field(default_factory=list)
    flavors: List[FlavorUpdateExtended] = Field(default_factory=list)
    identity_providers: List[IdentityProviderUpdateExtended] = Field(
        default_factory=list
    )
    images: List[ImageUpdateExtended] = Field(default_factory=list)
    projects: List[ProjectUpdateExtended] = Field(default_factory=list)
    services: List[ServiceUpdateExtended] = Field(default_factory=list)


class ProviderExtended(Provider):
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

    location: Optional[Location] = None
    clusters: List[ClusterExtended] = Field(default_factory=list)
    flavors: List[FlavorExtended] = Field(default_factory=list)
    identity_providers: List[IdentityProviderExtended] = Field(
        default_factory=list
    )
    images: List[ImageExtended] = Field(default_factory=list)
    projects: List[ProjectExtended] = Field(default_factory=list)
    services: List[ServiceExtended] = Field(default_factory=list)
