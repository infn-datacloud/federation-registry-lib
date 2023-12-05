"""Pydantic extended models of the User Group owned by an Identity Provider."""
from typing import List

from pydantic import Field

from app.identity_provider.schemas import (
    IdentityProviderRead,
    IdentityProviderReadPublic,
)
from app.project.schemas import ProjectRead, ProjectReadPublic
from app.sla.schemas import SLARead, SLAReadPublic
from app.user_group.schemas import UserGroupRead, UserGroupReadPublic


class SLAReadExtended(SLARead):
    """Model to extend the SLA data read from the DB with the lists of related items."""

    projects: List[ProjectRead] = Field(description="Involved Projects.")


class SLAReadExtendedPublic(SLAReadPublic):
    """Model to extend the SLA data read from the DB with the lists of related items."""

    projects: List[ProjectReadPublic] = Field(description="Involved Projects.")


class UserGroupReadExtended(UserGroupRead):
    """Model to extend the User Group data read from the DB with the lists of related
    items.
    """

    identity_provider: IdentityProviderRead = Field(
        description="Identity Provider owning this User Group."
    )
    slas: List[SLAReadExtended] = Field(
        description="List of SLAs involving this User Group.",
    )


class UserGroupReadExtendedPublic(UserGroupReadPublic):
    """Model to extend the User Group data read from the DB with the lists of related
    items.
    """

    identity_provider: IdentityProviderReadPublic = Field(
        description="Identity Provider owning this User Group."
    )
    slas: List[SLAReadExtendedPublic] = Field(
        description="List of SLAs involving this User Group.",
    )
