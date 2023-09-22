from typing import List

from app.provider.schemas import ProviderQuery
from app.provider.schemas_extended import ProviderCreateExtended, ProviderReadExtended
from models.cmdb.region import RegionWrite
from pydantic import BaseModel, Field


class Representation(BaseModel):
    def __str__(self) -> str:
        return f"{self.name}"


class ProviderWrite(ProviderCreateExtended, Representation):
    regions: List[RegionWrite] = Field(
        default_factory=list, description="List of regions"
    )
    # flavors: List[FlavorWrite] = Field(
    #    default_factory=list, description="List of flavors"
    # )
    # images: List[ImageWrite] = Field(default_factory=list,
    #  description="List of images")
    # projects: List[ProjectWrite] = Field(
    #    default_factory=list, description="List of projects"
    # )


class ProviderRead(ProviderReadExtended, Representation):
    pass


class ProviderQuery(ProviderQuery, Representation):
    pass
