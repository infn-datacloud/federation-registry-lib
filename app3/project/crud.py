from .models import Project as ProjectModel
from .schemas import ProjectCreate, ProjectUpdate
from ..crud import CRUDBase


class CRUDProject(CRUDBase[ProjectModel, ProjectCreate, ProjectUpdate]):
    """"""


project = CRUDProject(ProjectModel, ProjectCreate)
