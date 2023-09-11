from typing import List, Optional, Union

from app.identity_provider.schemas import (
    IdentityProviderRead,
    IdentityProviderReadPublic,
)
from app.project.schemas import ProjectRead, ProjectReadPublic
from app.provider.schemas import ProviderRead, ProviderReadPublic
from app.quota.schemas import QuotaRead, QuotaReadPublic
from app.service.schemas import (
    CinderServiceRead,
    CinderServiceReadPublic,
    KeystoneServiceRead,
    KeystoneServiceReadPublic,
    NovaServiceRead,
    NovaServiceReadPublic,
)
from app.sla.schemas import SLARead, SLAReadPublic
from app.user_group.schemas import UserGroupRead, UserGroupReadPublic
from pydantic import Field


class UserGroupReadExtended(UserGroupRead):
    """Model to extend the User Group data read from the DB with the lists of
    related items."""

    identity_provider: IdentityProviderRead = Field(
        description="Identity Provider owning this User Group."
    )


class UserGroupReadExtendedPublic(UserGroupReadPublic):
    """Model to extend the User Group data read from the DB with the lists of
    related items."""

    identity_provider: IdentityProviderReadPublic = Field(
        description="Identity Provider owning this User Group."
    )


class SLAReadExtended(SLARead):
    """Model to extend the SLA data read from the DB with the lists of related
    items."""

    user_group: UserGroupReadExtended = Field(description="Involved User Group.")


class SLAReadExtendedPublic(SLAReadPublic):
    """Model to extend the SLA data read from the DB with the lists of related
    items."""

    user_group: UserGroupReadExtendedPublic = Field(description="Involved User Group.")


class QuotaReadExtended(QuotaRead):
    """Model to extend the Quota data read from the DB with the lists of
    related items."""

    service: Union[CinderServiceRead, KeystoneServiceRead, NovaServiceRead] = Field(
        description="A generic Quota applies to only one generic Service."
    )


class QuotaReadExtendedPublic(QuotaReadPublic):
    """Model to extend the Quota data read from the DB with the lists of
    related items."""

    service: Union[
        CinderServiceReadPublic, KeystoneServiceReadPublic, NovaServiceReadPublic
    ] = Field(description="A generic Quota applies to only one generic Service.")


class ProjectReadExtended(ProjectRead):
    """Model to extend the Project data read from the DB with the lists of
    related items for authenticated users."""

    provider: ProviderRead = Field(description="Provider owning this Project.")
    quotas: List[QuotaReadExtended] = Field(
        default_factory=list, description="List of owned quotas."
    )
    sla: Optional[SLAReadExtended] = Field(
        default=None, description="SLA involving this Project."
    )


class ProjectReadExtendedPublic(ProjectReadPublic):
    """Model to extend the Project data read from the DB with the lists of
    related items for non-authenticated users."""

    provider: ProviderReadPublic = Field(description="Provider owning this Project.")
    quotas: List[QuotaReadExtendedPublic] = Field(
        default_factory=list, description="List of owned quotas."
    )
    sla: Optional[SLAReadExtendedPublic] = Field(
        default=None, description="SLA involving this Project."
    )
