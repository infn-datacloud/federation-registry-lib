from ..nodes.project import Project, ProjectCreate
from ..relationships.book_project import BookProject, BookProjectCreate


class ProjectCreateExtended(ProjectCreate):
    relationship: BookProjectCreate


class ProjectExtended(Project):
    relationship: BookProject
