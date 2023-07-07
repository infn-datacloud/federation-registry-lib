from pydantic import AnyHttpUrl
from typing import Optional

from .enum import ServiceType
from ..models import BaseNodeCreate, BaseNodeQuery, BaseNodeRead


class ServiceQuery(BaseNodeQuery):
    """Service Query Model class.

    Attributes:
        description (str | None): Brief description.
        endpoint (str | None): URL pointing to this service
    """

    endpoint: Optional[AnyHttpUrl] = None


class BaseService(BaseNodeCreate):
    """Service Create Model class.

    Class without id (which is populated by the database).
    Expected as input when performing a PATCH, PUT or POST request.

    Attributes:
        description (str): Brief description.
        endpoint (str): URL pointing to this service
        type (ServiceTypeUpdate): Service type.
    """

    endpoint: AnyHttpUrl


class ServiceCreate(BaseService):
    """Service Create Model class.

    Class without id (which is populated by the database).
    Expected as input when performing a PATCH, PUT or POST request.

    Attributes:
        description (str): Brief description.
        endpoint (str): URL pointing to this service
        type (ServiceTypeUpdate): Service type.
    """

    type: ServiceType


class ServiceUpdate(BaseService):
    """Service Create Model class.

    Class without id (which is populated by the database).
    Expected as input when performing a PATCH, PUT or POST request.

    Attributes:
        description (str): Brief description.
        endpoint (str): URL pointing to this service
        type (ServiceTypeUpdate): Service type.
    """


class Service(BaseNodeRead, BaseService):
    """Service class.

    Class retrieved from the database.
    Expected as output when performing a REST request.
    It contains all the non-sensible data written
    in the database.

    Attributes:
        uid (uuid): Unique ID.
        description (str): Brief description.
        endpoint (str): URL pointing to this service
        type (ServiceType): Service type.
    """


class NovaServiceQuery(ServiceQuery):
    pass


class NovaServiceCreate(BaseService):
    pass


class NovaServiceUpdate(ServiceUpdate):
    pass


class NovaService(Service):
    pass


class MesosServiceQuery(ServiceQuery):
    pass


class MesosServiceCreate(BaseService):
    pass


class MesosServiceUpdate(ServiceUpdate):
    pass


class MesosService(Service):
    pass


class ChronosServiceQuery(ServiceQuery):
    pass


class ChronosServiceCreate(BaseService):
    pass


class ChronosServiceUpdate(ServiceUpdate):
    pass


class ChronosService(Service):
    pass


class MarathonServiceQuery(ServiceQuery):
    pass


class MarathonServiceCreate(BaseService):
    pass


class MarathonServiceUpdate(ServiceUpdate):
    pass


class MarathonService(Service):
    pass


class KubernetesServiceQuery(ServiceQuery):
    pass


class KubernetesServiceCreate(BaseService):
    pass


class KubernetesServiceUpdate(ServiceUpdate):
    pass


class KubernetesService(Service):
    pass


class RucioServiceQuery(ServiceQuery):
    pass


class RucioServiceCreate(BaseService):
    pass


class RucioServiceUpdate(ServiceUpdate):
    pass


class RucioService(Service):
    pass


class OneDataServiceQuery(ServiceQuery):
    pass


class OneDataServiceCreate(BaseService):
    pass


class OneDataServiceUpdate(ServiceUpdate):
    pass


class OneDataService(Service):
    pass
