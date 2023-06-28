from neomodel import One, ZeroOrMore
from pydantic import Field, validator
from typing import List

from .schemas import Service, ServiceCreate, ServiceUpdate
from ..quota.schemas import Quota
from ..service_type.schemas import ServiceType, ServiceTypeCreate
from ..validators import get_all_nodes_from_rel, get_single_node_from_rel


class ServiceCreateExtended(ServiceCreate):
    type: ServiceTypeCreate


class ServiceUpdateExtended(ServiceUpdate):
    type: ServiceType
    quotas: List[Quota] = Field(default_factory=list)


class ServiceExtended(Service):
    type: ServiceType
    quotas: List[Quota] = Field(default_factory=list)

    @validator("type", pre=True)
    def get_single_service_type(cls, v: One) -> ServiceType:
        return get_single_node_from_rel(v)

    @validator("quotas", pre=True)
    def get_all_quotas(cls, v: ZeroOrMore) -> List[Quota]:
        return get_all_nodes_from_rel(v)
