from neomodel import One, ZeroOrMore
from pydantic import Field, validator
from typing import List

from .schemas import Service, ServiceCreate, ServiceUpdate
from ..quota.schemas import Quota
from ..service_type.schemas import ServiceType, ServiceTypeCreate


class ServiceCreateExtended(ServiceCreate):
    type: ServiceTypeCreate


class ServiceUpdateExtended(ServiceUpdate):
    type: ServiceType
    quotas: List[Quota] = Field(default_factory=list)


class ServiceExtended(Service):
    type: ServiceType
    quotas: List[Quota] = Field(default_factory=list)
