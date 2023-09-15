from app.project.schemas import ProjectCreate, ProjectQuery
from app.project.schemas_extended import ProjectReadExtended
from models.cmdb.quota import CinderQuotaWrite, NovaQuotaWrite
from pydantic import BaseModel


class Representation(BaseModel):
    def __str__(self) -> str:
        return f"{self.name}"


class ProjectWrite(ProjectCreate, Representation):
    compute_quota: NovaQuotaWrite
    block_storage_quota: CinderQuotaWrite


class ProjectRead(ProjectReadExtended, Representation):
    pass


class ProjectQuery(ProjectQuery, Representation):
    pass
