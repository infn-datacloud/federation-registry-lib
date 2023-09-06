import sys
from pathlib import Path
from typing import List, Optional

from pydantic import AnyHttpUrl, BaseModel, root_validator

external_path = Path.cwd().parent
sys.path.insert(1, str(external_path))

from app.location.schemas import LocationBase
from app.provider.schemas import ProviderBase


class IDP(BaseModel):
    name: str
    protocol: str
    group_claim: str
    endpoint: AnyHttpUrl


class Project(BaseModel):
    id: Optional[str]
    name: Optional[str]
    domain: Optional[str]

    @root_validator
    def check_id_or_name_and_domain(cls, values):
        if values.get("id") is not None:
            values["name"] = None
            values["domain"] = None
        else:
            assert (
                values["name"] is not None and values["domain"] is not None
            ), "If ID is None, both 'name' and 'domain' must be set"
        return values


class Openstack(ProviderBase):
    auth_url: str
    location: LocationBase
    identity_providers: List[IDP]
    projects: List[Project]


class Config(BaseModel):
    openstack: List[Openstack]
