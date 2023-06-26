from ..book_project.schemas import BookProject, BookProjectCreate
from ..project.schemas import Project, ProjectCreate


class ProjectCreateExtended(ProjectCreate):
    relationship: BookProjectCreate


class ProjectExtended(Project):
    relationship: BookProject
