from typing import List
from pydantic import Field, validator

from .schemas import Service
from ..provider.schemas import Provider
from ..quota.schemas import Quota
from ..validators import get_all_nodes_from_rel, get_single_node_from_rel


class ServiceExtended(Service):
    provider: Provider
    quotas: List[Quota] = Field(default_factory=list)

    _get_single_provider = validator("provider", pre=True, allow_reuse=True)(
        get_single_node_from_rel
    )

    _get_all_quotas = validator("quotas", pre=True, allow_reuse=True)(
        get_all_nodes_from_rel
    )
