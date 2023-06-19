from typing import List

from .service import Service
from ..relationships import Quota, ProvideService


class ServiceExtended(Service):
    quotas: List[Quota]
    details: ProvideService
