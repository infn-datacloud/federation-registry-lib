from app.project.models import Project 
from app.project.schemas import ProjectCreate, ProjectUpdate
from app.crud import CRUDBase


class CRUDProject(CRUDBase[Project, ProjectCreate, ProjectUpdate]):
    """"""


project = CRUDProject(Project, ProjectCreate)
