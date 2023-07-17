from app.project.models import Project as ProjectModel
from app.project.schemas import ProjectCreate, ProjectUpdate
from app.crud import CRUDBase


class CRUDProject(CRUDBase[ProjectModel, ProjectCreate, ProjectUpdate]):
    """"""


project = CRUDProject(ProjectModel, ProjectCreate)
