from app.sla.schemas import SLARead
from app.project.schemas import ProjectRead
from app.user_group.schemas import UserGroupRead


class SLAReadExtended(SLARead):
    project: ProjectRead
    user_group: UserGroupRead
