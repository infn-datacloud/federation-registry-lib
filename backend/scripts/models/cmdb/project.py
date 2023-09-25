from typing import List, Optional, Union

from app.project.schemas import ProjectCreate, ProjectQuery
from app.project.schemas_extended import ProjectReadExtended
from models.cmdb.quota import BlockStorageQuotaWrite, ComputeQuotaWrite
from models.cmdb.sla import SLAWrite
from pydantic import Field


class ProjectWrite(ProjectCreate):
    name: str = Field(alias="_id")
    quotas: List[Union[ComputeQuotaWrite, BlockStorageQuotaWrite]] = Field(
        default_factory=list, description="List of generic and per users quotas"
    )
    sla: Optional[SLAWrite] = Field(default=None, description="SLA")

    class Config:
        allow_population_by_field_name = True


class ProjectRead(ProjectReadExtended):
    pass


class ProjectQuery(ProjectQuery):
    pass
