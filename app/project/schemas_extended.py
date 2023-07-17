from pydantic import Field
from typing import List, Optional

from app.project.schemas import ProjectRead
from app.provider.schemas import ProviderRead
from app.quota.schemas_extended import QuotaReadExtended
from app.sla.schemas import SLARead
from app.user_group.schemas import UserGroupRead

class ProjectReadExtended(ProjectRead):
    provider: ProviderRead
    quotas: List[QuotaReadExtended] = Field(default_factory=list)
    sla: Optional[SLARead] = None
    user_group: Optional[UserGroupRead] = None
