"""Pydantic extended models of the User Group owned by an Identity Provider."""
from typing import List

from pydantic import Field

from app.identity_provider.schemas import (
    IdentityProviderRead,
    IdentityProviderReadPublic,
)
from app.project.schemas import ProjectRead, ProjectReadPublic
from app.provider.schemas import ProviderRead, ProviderReadPublic
from app.sla.schemas import SLARead, SLAReadPublic
from app.user_group.schemas import UserGroupRead, UserGroupReadPublic


class ProjectReadExtended(ProjectRead):
    """Model to extend the Project data read from the DB.

    Add the provider hosting it.
    """

    provider: ProviderRead = Field(description="Provider owning this project")


class ProjectReadExtendedPublic(ProjectReadPublic):
    """Model to extend the Project public data read from the DB.

    Add the provider hosting it.
    """

    provider: ProviderReadPublic = Field(description="Provider owning this project")


class SLAReadExtended(SLARead):
    """Model to extend the SLA data read from the DB.

    Add the list of accessible projects.
    """

    projects: List[ProjectReadExtended] = Field(description="Involved Projects.")


class SLAReadExtendedPublic(SLAReadPublic):
    """Model to extend the SLA public data read from the DB.

    Add the list of accessible projects.
    """

    projects: List[ProjectReadExtendedPublic] = Field(description="Involved Projects.")


class UserGroupReadExtended(UserGroupRead):
    """Model to extend the User Group data read from the DB.

    Add the identity provider owning it and the list of involved SLAs.
    """

    identity_provider: IdentityProviderRead = Field(
        description="Identity Provider owning this User Group."
    )
    slas: List[SLAReadExtended] = Field(
        description="List of SLAs involving this User Group.",
    )


class UserGroupReadExtendedPublic(UserGroupReadPublic):
    """Model to extend the User Group public data read from the DB.

    Add the identity provider owning it and the list of involved SLAs.
    """

    identity_provider: IdentityProviderReadPublic = Field(
        description="Identity Provider owning this User Group."
    )
    slas: List[SLAReadExtendedPublic] = Field(
        description="List of SLAs involving this User Group.",
    )
