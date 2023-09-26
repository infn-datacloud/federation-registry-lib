from typing import List

from app.crud import CRUDBase
from app.project.models import Project
from app.project.schemas_extended import SLAReadExtended, SLAReadExtendedPublic
from app.sla.models import SLA
from app.sla.schemas import SLACreate, SLARead, SLAReadPublic, SLAReadShort, SLAUpdate
from app.user_group.models import UserGroup


class CRUDSLA(
    CRUDBase[
        SLA,
        SLACreate,
        SLAUpdate,
        SLARead,
        SLAReadPublic,
        SLAReadShort,
        SLAReadExtended,
        SLAReadExtendedPublic,
    ]
):
    """"""

    def create(
        self,
        *,
        obj_in: SLACreate,
        projects: List[Project],
        user_group: UserGroup,
        force: bool = False
    ) -> SLA:
        db_obj = super().create(obj_in=obj_in, force=force)
        db_obj.user_group.connect(user_group)
        for i in projects:
            db_obj.projects.connect(i)
        return db_obj


sla = CRUDSLA(
    model=SLA,
    create_schema=SLACreate,
    read_schema=SLARead,
    read_public_schema=SLAReadPublic,
    read_short_schema=SLAReadShort,
    read_extended_schema=SLAReadExtended,
    read_extended_public_schema=SLAReadExtendedPublic,
)
