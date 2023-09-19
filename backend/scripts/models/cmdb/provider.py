from typing import List, Optional

from app.provider.schemas import ProviderQuery
from app.provider.schemas_extended import ProviderCreateExtended, ProviderReadExtended
from models.cmdb.flavor import FlavorWrite
from models.cmdb.image import ImageWrite
from models.cmdb.location import LocationWrite
from models.cmdb.project import ProjectWrite
from models.cmdb.service import ServiceWrite
from pydantic import BaseModel, Field


class Representation(BaseModel):
    def __str__(self) -> str:
        return f"{self.name}"


class ProviderWrite(ProviderCreateExtended, Representation):
    location: Optional[LocationWrite] = Field(
        default=None, description="Provider location"
    )
    flavors: List[FlavorWrite] = Field(
        default_factory=list, description="List of flavors"
    )
    images: List[ImageWrite] = Field(default_factory=list, description="List of images")
    projects: List[ProjectWrite] = Field(
        default_factory=list, description="List of projects"
    )
    services: List[ServiceWrite] = Field(
        default_factory=list, description="List of services"
    )


class ProviderRead(ProviderReadExtended, Representation):
    pass


class ProviderQuery(ProviderQuery, Representation):
    pass
