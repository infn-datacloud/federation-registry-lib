from pydantic import BaseModel, Field, validator
from typing import List, Optional
from uuid import UUID

from .cluster import Cluster, ClusterCreate
from .flavor import Flavor, FlavorCreate
from .identity_provider import IdentityProvider, IdentityProviderCreate
from .image import Image, ImageCreate
from .location import Location, LocationCreate
from .project import Project, ProjectCreate
from .service import Service, ServiceCreate
from ..utils import get_single_node_from_rel
from ..relationships import (
    AuthMethod,
    AuthMethodCreate,
    AvailableCluster,
    AvailableClusterCreate,
    AvailableVMFlavor,
    AvailableVMFlavorCreate,
    AvailableVMImage,
    AvailableVMImageCreate,
    BookProject,
    BookProjectCreate,
)


class ProviderIDPCreate(IdentityProviderCreate):
    relationship: AuthMethodCreate


class ProviderIDP(IdentityProvider):
    relationship: AuthMethod


class ProviderClusterCreate(ClusterCreate):
    relationship: AvailableClusterCreate


class ProviderCluster(Cluster):
    relationship: AvailableCluster


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


class ProviderBase(BaseModel):
    """Provider Base class

    Class without id (which is populated by the database).
    Expected as input when performing a PATCH REST request.

    Attributes:
        name (str): Provider name (type).
        description (str): Brief description.
        support_email (list of str): List of maintainers emails.
        is_public (bool): Public or private provider.
    """

    name: Optional[str] = None
    description: Optional[str] = None
    is_public: Optional[bool] = None
    support_email: Optional[List[str]] = None

    class Config:
        validate_assignment = True


class ProviderUpdate(ProviderBase):
    """Provider Base class

    Class without id (which is populated by the database).
    Expected as input when performing a PATCH REST request.

    Attributes:
        name (str): Provider name (type).
        description (str): Brief description.
        support_email (list of str): List of maintainers emails.
        is_public (bool): Public or private provider.
    """

    description: str = ""
    is_public: bool = False
    support_email: List[str] = Field(default_factory=list)
    location: Optional[LocationCreate] = None
    clusters: List[ProviderClusterCreate] = Field(default_factory=list)
    flavors: List[ProviderFlavorCreate] = Field(default_factory=list)
    identity_providers: List[ProviderIDPCreate] = Field(default_factory=list)
    images: List[ProviderImageCreate] = Field(default_factory=list)
    projects: List[ProviderProjectCreate] = Field(default_factory=list)
    services: List[ServiceCreate] = Field(default_factory=list)


class ProviderCreate(ProviderUpdate):
    """Provider Create class

    Class without id (which is populated by the database).
    Expected as input when performing a POST REST request.

    Attributes:
        name (str): Provider name (type).
        description (str): Brief description.
        support_email (list of str): List of maintainers emails.
        is_public (bool): Public or private provider.
    """

    name: str


class Provider(ProviderBase):
    """Provider class

    Class retrieved from the database
    expected as output when performing a REST request.
    It contains all the non-sensible data written
    in the database.

    Attributes:
        uid (uuid): Provider unique ID.
        name (str): Provider name (type).
        description (str): Brief description.
        support_email (list of str): List of maintainers emails.
        is_public (bool): Public or private provider.
    """

    uid: UUID
    location: Optional[Location] = None
    clusters: List[ProviderCluster] = Field(default_factory=list)
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
                ProviderCluster(
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

    @validator("services", pre=True)
    def get_all_services(cls, v):
        return v.all()

    class Config:
        orm_mode = True
