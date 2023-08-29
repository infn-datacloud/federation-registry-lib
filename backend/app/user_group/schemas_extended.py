from typing import List

from app.identity_provider.schemas import IdentityProviderRead
from app.project.schemas import ProjectRead
from app.provider.schemas import ProviderRead
from app.query import create_subquery_model
from app.service.schemas import ServiceQuery
from app.sla.schemas import SLARead
from app.user_group.schemas import UserGroupRead
from pydantic import Field


class ProjectReadExtended(ProjectRead):
    """Model to extend the SLA data read from the DB with the lists of related
    items."""

    provider: ProviderRead = Field(description="Provider owning this Project.")


class SLAReadExtended(SLARead):
    """Model to extend the SLA data read from the DB with the lists of related
    items."""

    project: ProjectRead = Field(description="Involved Project.")


class UserGroupReadExtended(UserGroupRead):
    """Model to extend the User Group data read from the DB with the lists of
    related items."""

    identity_provider: IdentityProviderRead = Field(
        default_factory=list,
        description="Identity Provider owning this User Group.",
    )
    slas: List[SLAReadExtended] = Field(
        default_factory=list,
        description="List of SLAs involving this User Group.",
    )


ServiceSubQuery = create_subquery_model(ServiceQuery)
# QuotaSubQuery = create_subquery_model(QuotaQuery)
