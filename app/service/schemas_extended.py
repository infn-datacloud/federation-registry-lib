from pydantic import Field
from typing import List

from .schemas import Service
from ..quota.schemas import ComputeTimeQuota


class NovaService(Service):
    compute_time_quotas: List[ComputeTimeQuota] = Field(default_factory=list)


class MesosService(Service):
    pass


class ChronosService(Service):
    pass


class MarathonService(Service):
    pass


class KubernetesService(Service):
    pass


class RucioService(Service):
    pass


class OneDataService(Service):
    pass
