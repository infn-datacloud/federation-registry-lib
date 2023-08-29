from typing import List

from app.identity_provider.schemas import IdentityProviderRead
from app.project.schemas import ProjectRead
from app.project.schemas_extended import QuotaReadExtended
from app.provider.schemas import ProviderRead
from app.sla.schemas import SLARead
from app.user_group.schemas import UserGroupRead
from pydantic import Field


class ProjectReadExtended(ProjectRead):
    """Model to extend the Project data read from the
    DB with the lists of related items.
    """

    provider: ProviderRead = Field(description="Provider owning this project")
    quotas: List[QuotaReadExtended] = Field(
        default_factory=list,
        description="List of quotas owned by this Project.",
    )


class UserGroupReadExtended(UserGroupRead):
    """Model to extend the User Group data read from the
    DB with the lists of related items.
    """

    identity_provider: IdentityProviderRead = Field(
        description="Identity Provider owning this User Group."
    )


class SLAReadExtended(SLARead):
    """Model to extend the SLA data read from the
    DB with the lists of related items.
    """

    project: ProjectReadExtended = Field(description="Involved Project.")
    user_group: UserGroupReadExtended = Field(
        description="Involved User Group."
    )
