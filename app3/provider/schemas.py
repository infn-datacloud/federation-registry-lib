from neomodel import ZeroOrMore
from pydantic import EmailStr, Field, validator
from typing import List, Optional

from ..auth_method.schemas import AuthMethod, AuthMethodCreate
from ..available_cluster.schemas import (
    AvailableCluster,
    AvailableClusterCreate,
)
from ..available_vm_flavor.schemas import (
    AvailableVMFlavor,
    AvailableVMFlavorCreate,
)
from ..available_vm_image.schemas import (
    AvailableVMImage,
    AvailableVMImageCreate,
)
from ..book_project.schemas import BookProject, BookProjectCreate
from ..cluster.schemas import Cluster, ClusterCreate
from ..flavor.schemas import Flavor, FlavorCreate
from ..identity_provider.schemas import (
    IdentityProvider,
    IdentityProviderCreate,
)
from ..image.schemas import Image, ImageCreate
from ..location.schemas import Location, LocationCreate
from ..models import BaseNodeCreate, BaseNodeQuery, BaseNodeRead
from ..project.schemas import Project, ProjectCreate
from ..service.schemas import Service, ServiceCreate
from ..validators import (
    get_all_nodes_from_rel,
    get_all_nodes_with_rel_data,
    get_single_node_from_rel,
)


class ClusterCreateExtended(ClusterCreate):
    relationship: AvailableClusterCreate


class ClusterExtended(Cluster):
    relationship: AvailableCluster


class FlavorCreateExtended(FlavorCreate):
    relationship: AvailableVMFlavorCreate


class FlavorExtended(Flavor):
    relationship: AvailableVMFlavor


class IdentityProviderCreateExtended(IdentityProviderCreate):
    relationship: AuthMethodCreate


class IdentityProviderExtended(IdentityProvider):
    relationship: AuthMethod


class ImageCreateExtended(ImageCreate):
    relationship: AvailableVMImageCreate


class ImageExtended(Image):
    relationship: AvailableVMImage


class ProjectCreateExtended(ProjectCreate):
    relationship: BookProjectCreate


class ProjectExtended(Project):
    relationship: BookProject


class ProviderQuery(BaseNodeQuery):
    """Provider Query Model class.

    Attributes:
        description (str | None): Brief description.
        name (str | None): Provider name (type).
        is_public (bool | None): Public or private provider.
        support_email (list of str | None): List of maintainers emails.
    """

    name: Optional[str] = None
    is_public: Optional[bool] = None
    support_email: Optional[List[EmailStr]] = None


class ProviderPatch(BaseNodeCreate):
    """Provider Patch Model class.

    Class without id (which is populated by the database).
    Expected as input when performing a PATCH request.

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

    name: Optional[str] = None
    is_public: bool = False
    support_email: List[EmailStr] = Field(default_factory=list)
    location: Optional[LocationCreate] = None
    clusters: List[ClusterCreateExtended] = Field(default_factory=list)
    flavors: List[FlavorCreateExtended] = Field(default_factory=list)
    identity_providers: List[IdentityProviderCreateExtended] = Field(
        default_factory=list
    )
    images: List[ImageCreateExtended] = Field(default_factory=list)
    projects: List[ProjectCreateExtended] = Field(default_factory=list)
    services: List[ServiceCreate] = Field(default_factory=list)


class ProviderCreate(ProviderPatch):
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

    name: str


class Provider(ProviderCreate, BaseNodeRead):
    """Providerclass.

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
