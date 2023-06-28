from .models import Project as ProjectModel
from .schemas import ProjectCreate, ProjectPatch
from ..crud import CRUDBase


class CRUDProject(CRUDBase[ProjectModel, ProjectCreate, ProjectPatch]):
    """"""


project = CRUDProject(ProjectModel, ProjectCreate)
