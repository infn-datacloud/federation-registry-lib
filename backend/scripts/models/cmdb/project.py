from typing import List, Optional, Union

from app.project.schemas import ProjectCreate, ProjectQuery
from app.project.schemas_extended import ProjectReadExtended
from models.cmdb.quota import BlockStorageQuotaWrite, ComputeQuotaWrite
from models.cmdb.sla import SLAWrite
from pydantic import BaseModel, Field


class Representation(BaseModel):
    def __str__(self) -> str:
        if self.name is not None:
            return f"{self.name}"
        if self.uuid is not None:
            return f"{self.uuid}"
        return super().__str__()


class ProjectWrite(ProjectCreate, Representation):
    quotas: List[Union[ComputeQuotaWrite, BlockStorageQuotaWrite]] = Field(
        default_factory=list, description="List of generic and per users quotas"
    )
    sla: Optional[SLAWrite] = Field(default=None, description="SLA")


class ProjectRead(ProjectReadExtended, Representation):
    pass


class ProjectQuery(ProjectQuery, Representation):
    pass
