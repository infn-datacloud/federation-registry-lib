from neomodel import ZeroOrMore
from pydantic import Field, validator
from typing import List, Optional

from .schemas import Provider, ProviderCreate, ProviderPatch
from ..cluster.schemas import Cluster
from ..cluster.schemas_extended import ClusterExtended, ClusterCreateExtended
from ..flavor.schemas import Flavor
from ..flavor.schemas_extended import FlavorExtended, FlavorCreateExtended
from ..identity_provider.schemas import IdentityProvider
from ..identity_provider.schemas_extended import (
    IdentityProviderExtended,
    IdentityProviderCreateExtended,
)
from ..image.schemas import Image
from ..image.schemas_extended import ImageExtended, ImageCreateExtended
from ..location.schemas import Location, LocationCreate
from ..project.schemas import Project
from ..project.schemas_extended import ProjectExtended, ProjectCreateExtended
from ..service.schemas import Service, ServiceCreate
from ..validators import (
    get_all_nodes_from_rel,
    get_all_nodes_with_rel_data,
    get_single_node_from_rel,
)


class ProviderPatchExtended(ProviderPatch):
    """Provider Patch Model class.

    Class without id (which is populated by the database).
    Expected as input when performing a PATCH request.

    Attributes:
        description (str | None): Brief description.
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
    services: List[ServiceCreate] = Field(default_factory=list)


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
    services: List[ServiceCreate] = Field(default_factory=list)


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
    services: List[Service] = Field(default_factory=list)

    _get_single_location = validator("location", pre=True, allow_reuse=True)(
        get_single_node_from_rel
    )

    _get_all_services = validator("services", pre=True, allow_reuse=True)(
        get_all_nodes_from_rel
    )

    @validator("clusters", pre=True)
    def get_all_clusters(cls, v: ZeroOrMore):
        return get_all_nodes_with_rel_data(Cluster, v)

    @validator("flavors", pre=True)
    def get_all_flavors(cls, v: ZeroOrMore):
        return get_all_nodes_with_rel_data(Flavor, v)

    @validator("identity_providers", pre=True)
    def get_all_identity_providers(cls, v: ZeroOrMore):
        return get_all_nodes_with_rel_data(IdentityProvider, v)

    @validator("images", pre=True)
    def get_all_images(cls, v: ZeroOrMore):
        return get_all_nodes_with_rel_data(Image, v)

    @validator("projects", pre=True)
    def get_all_projects(cls, v: ZeroOrMore):
        return get_all_nodes_with_rel_data(Project, v)
