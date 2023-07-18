from pydantic import Field
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


class UserGroupReadExtended(UserGroupRead):
    identity_provider: IdentityProviderRead


class SLAReadExtended(SLARead):
    user_group: UserGroupReadExtended


class QuotaReadExtended(QuotaRead):
    service: Union[
        ChronosServiceRead,
        KubernetesServiceRead,
        MarathonServiceRead,
        MesosServiceRead,
        NovaServiceRead,
        OneDataServiceRead,
        RucioServiceRead,
    ]


class ProjectReadExtended(ProjectRead):
    flavors: List[FlavorRead] = Field(default_factory=list)
    images: List[ImageRead] = Field(default_factory=list)
    provider: ProviderRead
    quotas: List[QuotaReadExtended] = Field(default_factory=list)
    sla: Optional[SLAReadExtended] = None
