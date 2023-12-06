"""Pydantic extended models of the SLA between a Project and a User Group."""
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

    Attributes:
    ----------
        uid (uuid): AssociatedProject unique ID.
        description (str): Brief description.
        name (str): Name of the project in the Provider.
        uuid (uuid): Project Unique ID in the Provider.
        provider (ProviderRead): Hosting provider.
    """

    provider: ProviderRead = Field(description="Provider owning this project")


class ProjectReadExtendedPublic(ProjectReadPublic):
    """Model to extend the Project public data read from the DB.

    Attributes:
    ----------
        uid (uuid): AssociatedProject unique ID.
        description (str): Brief description.
        name (str): Name of the project in the Provider.
        uuid (uuid): Project Unique ID in the Provider.
        provider (ProviderReadPublic): Hosting provider.
    """

    provider: ProviderReadPublic = Field(description="Provider owning this project")


class UserGroupReadExtended(UserGroupRead):
    """Model to extend the User Group data read from the DB.

    Attributes:
    ----------
        uid (int): User Group unique ID.
        description (str): Brief description.
        name (str): User Group name.
        identity_provider (IdentityProviderRead): Identity provider owning this
            user group.
    """

    identity_provider: IdentityProviderRead = Field(
        description="Identity Provider owning this User Group."
    )


class UserGroupReadExtendedPublic(UserGroupReadPublic):
    """Model to extend the User Group public data read from the DB.

    Attributes:
    ----------
        uid (int): User Group unique ID.
        description (str): Brief description.
        name (str): User Group name.
        identity_provider (IdentityProviderReadPublic): Identity provider owning this
            user group.
    """

    identity_provider: IdentityProviderReadPublic = Field(
        description="Identity Provider owning this User Group."
    )


class SLAReadExtended(SLARead):
    """Model to extend the SLA data read from the DB.

    Attributes:
    ----------
        uid (int): SLA unique ID.
        description (str): Brief description.
        doc_uuid (str): Unique ID of the document with the SLA details.
        start_date (datetime): SLA validity start date.
        end_date (datetime): SLA validity end date.
        projects (list of ProjectReadExtended): Target projects.
        user_group (UserGroupReadExtended): Target user group.
    """

    projects: List[ProjectReadExtended] = Field(description="Involved Projects.")
    user_group: UserGroupReadExtended = Field(description="Involved User Group.")


class SLAReadExtendedPublic(SLAReadPublic):
    """Model to extend the SLA public data read from the DB.

    Attributes:
    ----------
        uid (int): SLA unique ID.
        description (str): Brief description.
        doc_uuid (str): Unique ID of the document with the SLA details.
        projects (list of ProjectReadExtendedPublic): Target projects.
        user_group (UserGroupReadExtendedPublic): Target user group.
    """

    projects: List[ProjectReadExtendedPublic] = Field(description="Involved Projects.")
    user_group: UserGroupReadExtendedPublic = Field(description="Involved User Group.")
