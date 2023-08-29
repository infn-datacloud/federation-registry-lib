from typing import List, Optional, Union

from app.flavor.schemas import FlavorRead
from app.identity_provider.schemas import IdentityProviderRead
from app.image.schemas import ImageRead
from app.project.schemas import ProjectRead
from app.provider.schemas import ProviderRead
from app.quota.schemas import QuotaRead
from app.service.schemas import (
    ChronosServiceRead,
    KubernetesServiceRead,
    MarathonServiceRead,
    MesosServiceRead,
    NovaServiceRead,
    OneDataServiceRead,
    RucioServiceRead,
)
from app.sla.schemas import SLARead
from app.user_group.schemas import UserGroupRead
from pydantic import Field


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

    user_group: UserGroupReadExtended = Field(
        description="Involved User Group."
    )


class QuotaReadExtended(QuotaRead):
    """Model to extend the Quota data read from the
    DB with the lists of related items.
    """

    service: Union[
        ChronosServiceRead,
        KubernetesServiceRead,
        MarathonServiceRead,
        MesosServiceRead,
        NovaServiceRead,
        OneDataServiceRead,
        RucioServiceRead,
    ] = Field(
        description="A generic Quota applies to only one generic Service."
    )


class ProjectReadExtended(ProjectRead):
    """Model to extend the Project data read from the
    DB with the lists of related items.
    """

    flavors: List[FlavorRead] = Field(
        default_factory=list, description="List of usable Flavors."
    )
    images: List[ImageRead] = Field(
        default_factory=list, description="List of usable Images."
    )
    provider: ProviderRead = Field(description="Provider owning this Project.")
    quotas: List[QuotaReadExtended] = Field(
        default_factory=list, description="List of owned quotas."
    )
    sla: Optional[SLAReadExtended] = Field(
        default=None, description="SLA involving this Project."
    )
