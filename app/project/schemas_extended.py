from pydantic import Field
from typing import List, Optional

from app.project.schemas import ProjectRead
from app.provider.schemas import ProviderRead
from app.quota.schemas_extended import QuotaReadExtended
from app.sla.schemas import SLARead
from app.user_group.schemas import UserGroupRead


class SLAReadExtended(SLARead):
    user_group: UserGroupRead


class ProjectReadExtended(ProjectRead):
    provider: ProviderRead
    quotas: List[QuotaReadExtended] = Field(default_factory=list)
    sla: Optional[SLAReadExtended] = None
