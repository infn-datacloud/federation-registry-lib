from app.crud import CRUDBase
from app.project.models import Project
from app.sla.models import SLA
from app.sla.schemas import SLACreate, SLAUpdate
from app.user_group.models import UserGroup


class CRUDSLA(CRUDBase[SLA, SLACreate, SLAUpdate]):
    """"""

    def create(
        self,
        *,
        obj_in: SLACreate,
        project: Project,
        user_group: UserGroup,
        force: bool = False
    ) -> SLA:
        db_obj = super().create(obj_in=obj_in, force=force)
        db_obj.project.connect(project)
        db_obj.user_group.connect(user_group)
        return db_obj


sla = CRUDSLA(SLA, SLACreate)
