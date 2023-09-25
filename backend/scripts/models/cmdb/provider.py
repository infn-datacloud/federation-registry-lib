from typing import List

from app.provider.schemas import ProviderQuery
from app.provider.schemas_extended import ProviderCreateExtended, ProviderReadExtended
from models.cmdb.identity_provider import IdentityProviderWrite
from models.cmdb.region import RegionWrite
from pydantic import Field


class ProviderWrite(ProviderCreateExtended):
    name: str = Field(alias="_id")
    regions: List[RegionWrite] = Field(
        default_factory=list, description="List of regions"
    )
    identity_providers: List[IdentityProviderWrite] = Field(
        default_factory=list, description="List of supported identity providers"
    )

    class Config:
        allow_population_by_field_name = True


class ProviderRead(ProviderReadExtended):
    pass


class ProviderQuery(ProviderQuery):
    pass
