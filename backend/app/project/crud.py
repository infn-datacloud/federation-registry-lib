from app.crud import CRUDBase
from app.project.models import Project
from app.project.schemas import ProjectCreate, ProjectUpdate
from app.provider.models import Provider
from app.quota.crud import quota
from app.sla.crud import sla


class CRUDProject(CRUDBase[Project, ProjectCreate, ProjectUpdate]):
    """"""

    def create(
        self, *, obj_in: ProjectCreate, provider: Provider, force: bool = False
    ) -> Project:
        db_obj = super().create(obj_in=obj_in, force=force)
        db_obj.provider.connect(provider)
        return db_obj

    def remove(self, *, db_obj: Project) -> bool:
        for item in db_obj.quotas.all():
            quota.remove(item)
        item = db_obj.sla.single()
        if item is not None:
            sla.remove(item)
        return super().remove(db_obj=db_obj)


project = CRUDProject(Project, ProjectCreate)