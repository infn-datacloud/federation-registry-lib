"""Pydantic extended models of the User Group owned by an Identity Provider."""


from pydantic import BaseModel, Field

from fed_reg.identity_provider.schemas import (
    IdentityProviderRead,
    IdentityProviderReadPublic,
)
from fed_reg.models import BaseReadPrivateExtended, BaseReadPublicExtended
from fed_reg.project.constants import DOC_EXT_PROV
from fed_reg.project.schemas import ProjectRead, ProjectReadPublic
from fed_reg.provider.schemas import ProviderRead, ProviderReadPublic
from fed_reg.sla.constants import DOC_EXT_PROJ
from fed_reg.sla.schemas import SLARead, SLAReadPublic
from fed_reg.user_group.constants import DOC_EXT_IDP, DOC_EXT_SLA
from fed_reg.user_group.schemas import UserGroupRead, UserGroupReadPublic


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

    provider: ProviderRead = Field(description=DOC_EXT_PROV)


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

    provider: ProviderReadPublic = Field(description=DOC_EXT_PROV)


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
    """

    projects: list[ProjectReadExtended] = Field(description=DOC_EXT_PROJ)


class SLAReadExtendedPublic(SLAReadPublic):
    """Model to extend the SLA public data read from the DB.

    Attributes:
    ----------
        uid (int): SLA unique ID.
        description (str): Brief description.
        doc_uuid (str): Unique ID of the document with the SLA details.
        projects (list of ProjectReadExtended): Target projects.
    """

    projects: list[ProjectReadExtendedPublic] = Field(description=DOC_EXT_PROJ)


class UserGroupReadExtended(UserGroupRead, BaseReadPrivateExtended):
    """Model to extend the User Group data read from the DB.

    Attributes:
    ----------
        uid (int): User Group unique ID.
        description (str): Brief description.
        name (str): User Group name.
        identity_provider (IdentityProviderRead): Identity provider owning this
            user group.
        slas (list of SLAReadExtended): Owned SLAs.
    """

    identity_provider: IdentityProviderRead = Field(description=DOC_EXT_IDP)
    slas: list[SLAReadExtended] = Field(description=DOC_EXT_SLA)


class UserGroupReadExtendedPublic(UserGroupReadPublic, BaseReadPublicExtended):
    """Model to extend the User Group public data read from the DB.

    Attributes:
    ----------
        uid (int): User Group unique ID.
        description (str): Brief description.
        name (str): User Group name.
        identity_provider (IdentityProviderReadPublic): Identity provider owning this
            user group.
        slas (list of SLAReadExtendedPublic): Owned SLAs.
    """

    identity_provider: IdentityProviderReadPublic = Field(description=DOC_EXT_IDP)
    slas: list[SLAReadExtendedPublic] = Field(description=DOC_EXT_SLA)


class UserGroupReadSingle(BaseModel):
    __root__: UserGroupReadExtended | UserGroupRead | UserGroupReadExtendedPublic | UserGroupReadPublic = Field(
        ..., discriminator="schema_type"
    )


class UserGroupReadMulti(BaseModel):
    __root__: list[UserGroupReadExtended] | list[UserGroupRead] | list[
        UserGroupReadExtendedPublic
    ] | list[UserGroupReadPublic] = Field(..., discriminator="schema_type")
