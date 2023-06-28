from ..book_project.schemas import (
    BookProject,
    BookProjectCreate,
    BookProjectUpdate,
)
from ..project.schemas import Project, ProjectCreate, ProjectUpdate


class ProjectCreateExtended(ProjectCreate):
    relationship: BookProjectCreate


class ProjectUpdateExtended(ProjectUpdate):
    relationship: BookProjectUpdate


class ProjectExtended(Project):
    relationship: BookProject
