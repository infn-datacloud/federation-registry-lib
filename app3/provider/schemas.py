from pydantic import EmailStr, Field
from typing import List, Optional

from ..models import BaseNodeCreate, BaseNodeQuery, BaseNodeRead


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
    # location: Optional[LocationCreate] = None
    # clusters: List[ClusterCreateExtended] = Field(default_factory=list)
    # flavors: List[FlavorCreateExtended] = Field(default_factory=list)
    # identity_providers: List[IdentityProviderCreateExtended] = Field(
    #    default_factory=list
    # )
    # images: List[ImageCreateExtended] = Field(default_factory=list)
    # projects: List[ProjectCreateExtended] = Field(default_factory=list)
    # services: List[ServiceCreate] = Field(default_factory=list)


class Provider(BaseNodeRead):
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

    name: str
    is_public: bool = False
    support_email: List[EmailStr] = Field(default_factory=list)
