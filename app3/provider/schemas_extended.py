from neomodel import ZeroOrMore
from pydantic import Field, validator
from typing import List, Optional

from .schemas import Provider, ProviderCreate, ProviderUpdate
from ..cluster.schemas import Cluster
from ..cluster.schemas_extended import (
    ClusterExtended,
    ClusterCreateExtended,
    ClusterUpdateExtended,
)
from ..flavor.schemas import Flavor
from ..flavor.schemas_extended import (
    FlavorExtended,
    FlavorCreateExtended,
    FlavorUpdateExtended,
)
from ..identity_provider.schemas import IdentityProvider
from ..identity_provider.schemas_extended import (
    IdentityProviderExtended,
    IdentityProviderCreateExtended,
    IdentityProviderUpdateExtended,
)
from ..image.schemas import Image
from ..image.schemas_extended import (
    ImageExtended,
    ImageCreateExtended,
    ImageUpdateExtended,
)
from ..location.schemas import Location, LocationCreate, LocationUpdate
from ..project.schemas import Project
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
from ..validators import (
    get_all_nodes_from_rel,
    get_all_nodes_with_rel_data,
    get_single_node_from_rel,
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

    @validator("location", pre=True)
    def get_single_loc(cls, v: ZeroOrMore) -> Location:
        return get_single_node_from_rel(v)

    @validator("services", pre=True)
    def get_all_services(cls, v: ZeroOrMore) -> List[ServiceExtended]:
        return get_all_nodes_from_rel(v)

    @validator("clusters", pre=True)
    def get_all_clusters(cls, v: ZeroOrMore) -> List[ClusterExtended]:
        return get_all_nodes_with_rel_data(Cluster, v)

    @validator("flavors", pre=True)
    def get_all_flavors(cls, v: ZeroOrMore) -> List[FlavorExtended]:
        return get_all_nodes_with_rel_data(Flavor, v)

    @validator("identity_providers", pre=True)
    def get_all_identity_providers(
        cls, v: ZeroOrMore
    ) -> List[IdentityProviderExtended]:
        return get_all_nodes_with_rel_data(IdentityProvider, v)

    @validator("images", pre=True)
    def get_all_images(cls, v: ZeroOrMore) -> List[ImageExtended]:
        return get_all_nodes_with_rel_data(Image, v)

    @validator("projects", pre=True)
    def get_all_projects(cls, v: ZeroOrMore):
        return get_all_nodes_with_rel_data(Project, v)
