from pydantic import EmailStr, Field, validator
from typing import List, Optional

from .location import Location, LocationCreate
from .service import Service, ServiceCreate
from ..extended.cluster import ClusterCreateExtended, ClusterExtended
from ..extended.flavor import FlavorCreateExtended, FlavorExtended
from ..extended.identity_provider import (
    IdentityProviderCreateExtended,
    IdentityProviderExtended,
)
from ..extended.image import ImageCreateExtended, ImageExtended
from ..extended.project import ProjectCreateExtended, ProjectExtended
from ..utils.base_model import BaseNodeCreate, BaseNodeQuery, BaseNodeRead
from ..utils.validators import get_all_nodes_from_rel, get_single_node_from_rel


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
                FlavorExtended(
                    **node.__dict__, relationship=v.relationship(node)
                )
            )
        return flavors

    @validator("identity_providers", pre=True)
    def get_all_identity_providers(cls, v):
        identity_providers = []
        for node in v.all():
            identity_providers.append(
                IdentityProviderExtended(
                    **node.__dict__, relationship=v.relationship(node)
                )
            )
        return identity_providers

    @validator("images", pre=True)
    def get_all_images(cls, v):
        images = []
        for node in v.all():
            images.append(
                ImageExtended(
                    **node.__dict__, relationship=v.relationship(node)
                )
            )
        return images

    @validator("projects", pre=True)
    def get_all_projects(cls, v):
        projects = []
        for node in v.all():
            projects.append(
                ProjectExtended(
                    **node.__dict__, relationship=v.relationship(node)
                )
            )
        return projects
