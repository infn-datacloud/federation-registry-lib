from pydantic import Field
from typing import List, Optional

from app.flavor.schemas import FlavorRead
from app.identity_provider.schemas import IdentityProviderRead
from app.image.schemas import ImageRead
from app.project.schemas import ProjectRead
from app.provider.schemas import ProviderRead
from app.quota.schemas import QuotaRead
from app.service.schemas import ServiceRead
from app.sla.schemas import SLARead
from app.user_group.schemas import UserGroupRead


class UserGroupReadExtended(UserGroupRead):
    identity_provider: IdentityProviderRead


class SLAReadExtended(SLARead):
    user_group: UserGroupReadExtended


class QuotaReadExtended(QuotaRead):
    service: ServiceRead


class ProjectReadExtended(ProjectRead):
    flavors: List[FlavorRead] = Field(default_factory=list)
    images: List[ImageRead] = Field(default_factory=list)
    provider: ProviderRead
    quotas: List[QuotaReadExtended] = Field(default_factory=list)
    sla: Optional[SLAReadExtended] = None
