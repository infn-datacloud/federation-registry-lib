from app.project.schemas import ProjectRead
from app.provider.schemas import ProviderRead
from app.quota.schemas import QuotaRead
from app.service.schemas import ServiceRead

class ProjectReadExtended(ProjectRead):
    provider: ProviderRead
    
class QuotaReadExtended(QuotaRead):
    project: ProjectReadExtended
    service: ServiceRead
