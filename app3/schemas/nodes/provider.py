from pydantic import EmailStr, Field, validator
from typing import List, Optional

from .flavor import Flavor, FlavorCreate
from .identity_provider import IdentityProvider, IdentityProviderCreate
from .image import Image, ImageCreate
from .location import Location, LocationCreate
from .project import Project, ProjectCreate
from .service import Service, ServiceCreate
from ..extended.cluster import ClusterCreateExtended, ClusterExtended
from ..relationships.auth_method import AuthMethod, AuthMethodCreate
from ..relationships.available_vm_flavor import (
    AvailableVMFlavor,
    AvailableVMFlavorCreate,
)
from ..relationships.available_vm_image import (
    AvailableVMImage,
    AvailableVMImageCreate,
)
from ..relationships.book_project import BookProject, BookProjectCreate
from ..utils.base_model import BaseNodeCreate, BaseNodeQuery, BaseNodeRead
from ..utils.validators import get_all_nodes_from_rel, get_single_node_from_rel


class ProviderIDPCreate(IdentityProviderCreate):
    relationship: AuthMethodCreate


class ProviderIDP(IdentityProvider):
    relationship: AuthMethod


class ProviderFlavorCreate(FlavorCreate):
    relationship: AvailableVMFlavorCreate


class ProviderFlavor(Flavor):
    relationship: AvailableVMFlavor


class ProviderImageCreate(ImageCreate):
    relationship: AvailableVMImageCreate


class ProviderImage(Image):
    relationship: AvailableVMImage


class ProviderProjectCreate(ProjectCreate):
    relationship: BookProjectCreate


class ProviderProject(Project):
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
    flavors: List[ProviderFlavorCreate] = Field(default_factory=list)
    identity_providers: List[ProviderIDPCreate] = Field(default_factory=list)
    images: List[ProviderImageCreate] = Field(default_factory=list)
    projects: List[ProviderProjectCreate] = Field(default_factory=list)
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
    flavors: List[ProviderFlavor] = Field(default_factory=list)
    identity_providers: List[ProviderIDP] = Field(default_factory=list)
    images: List[ProviderImage] = Field(default_factory=list)
    projects: List[ProviderProject] = Field(default_factory=list)
    services: List[Service] = Field(default_factory=list)

    _get_single_location = validator("location", pre=True, allow_reuse=True)(
        get_single_node_from_rel
    )

    @validator("clusters", pre=True)
    def get_all_clusters(cls, v):
        clusters = []
        for node in v.all():
            clusters.append(
                ClusterExtended(
                    **node.__dict__, relationship=v.relationship(node)
                )
            )
        return clusters

    @validator("flavors", pre=True)
    def get_all_flavors(cls, v):
        flavors = []
        for node in v.all():
            flavors.append(
                ProviderFlavor(
                    **node.__dict__, relationship=v.relationship(node)
                )
            )
        return flavors

    @validator("identity_providers", pre=True)
    def get_all_identity_providers(cls, v):
        identity_providers = []
        for node in v.all():
            identity_providers.append(
                ProviderIDP(**node.__dict__, relationship=v.relationship(node))
            )
        return identity_providers

    @validator("images", pre=True)
    def get_all_images(cls, v):
        images = []
        for node in v.all():
            images.append(
                ProviderImage(
                    **node.__dict__, relationship=v.relationship(node)
                )
            )
        return images

    @validator("projects", pre=True)
    def get_all_projects(cls, v):
        projects = []
        for node in v.all():
            projects.append(
                ProviderProject(
                    **node.__dict__, relationship=v.relationship(node)
                )
            )
        return projects

    _get_all_services = validator("services", pre=True, allow_reuse=True)(
        get_all_nodes_from_rel
    )
