from typing import List
from pydantic import Field, validator

from .schemas import Service, ServiceCreate
from ..quota.schemas import Quota
from ..service_type.schemas import ServiceType, ServiceTypeCreate
from ..validators import get_all_nodes_from_rel, get_single_node_from_rel


class ServiceCreateExtended(ServiceCreate):
    type: ServiceTypeCreate


class ServiceExtended(Service):
    type: ServiceType
    quotas: List[Quota] = Field(default_factory=list)

    _get_single_service_type = validator("type", pre=True, allow_reuse=True)(
        get_single_node_from_rel
    )
    _get_all_quotas = validator("quotas", pre=True, allow_reuse=True)(
        get_all_nodes_from_rel
    )
