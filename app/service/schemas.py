from pydantic import AnyHttpUrl, BaseModel
from typing import Optional

from app.service.enum import ServiceType
from app.models import BaseNodeCreate, BaseNodeQuery, BaseNodeRead


class ServiceBase(BaseModel):
    """Service Create Model class.

    Class without id (which is populated by the database).
    Expected as input when performing a PATCH, PUT or POST request.

    Attributes:
        description (str): Brief description.
        endpoint (str): URL pointing to this service
        type (ServiceTypeUpdate): Service type.
    """

    endpoint: AnyHttpUrl
    type: ServiceType


class ServiceQuery(BaseNodeQuery):
    """Service Query Model class.

    Attributes:
        description (str | None): Brief description.
        endpoint (str | None): URL pointing to this service
    """

    endpoint: Optional[AnyHttpUrl] = None
    type: Optional[ServiceType] = None


class ServiceCreate(BaseNodeCreate, ServiceBase):
    """Service Create Model class.

    Class without id (which is populated by the database).
    Expected as input when performing a PATCH, PUT or POST request.

    Attributes:
        description (str): Brief description.
        endpoint (str): URL pointing to this service
        type (ServiceTypeUpdate): Service type.
    """


class ServiceUpdate(ServiceBase):
    """Service Create Model class.

    Class without id (which is populated by the database).
    Expected as input when performing a PATCH, PUT or POST request.

    Attributes:
        description (str): Brief description.
        endpoint (str): URL pointing to this service
        type (ServiceTypeUpdate): Service type.
    """


class ServiceRead(BaseNodeRead, ServiceBase):
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


class NovaServiceCreate(ServiceCreate):
    pass


class NovaServiceUpdate(ServiceUpdate):
    pass


class NovaServiceRead(ServiceRead):
    pass


class MesosServiceQuery(ServiceQuery):
    pass


class MesosServiceCreate(ServiceCreate):
    pass


class MesosServiceUpdate(ServiceUpdate):
    pass


class MesosServiceRead(ServiceRead):
    pass


class ChronosServiceQuery(ServiceQuery):
    pass


class ChronosServiceCreate(ServiceCreate):
    pass


class ChronosServiceUpdate(ServiceUpdate):
    pass


class ChronosServiceRead(ServiceRead):
    pass


class MarathonServiceQuery(ServiceQuery):
    pass


class MarathonServiceCreate(ServiceCreate):
    pass


class MarathonServiceUpdate(ServiceUpdate):
    pass


class MarathonServiceRead(ServiceRead):
    pass


class KubernetesServiceQuery(ServiceQuery):
    pass


class KubernetesServiceCreate(ServiceCreate):
    pass


class KubernetesServiceUpdate(ServiceUpdate):
    pass


class KubernetesServiceRead(ServiceRead):
    pass


class RucioServiceQuery(ServiceQuery):
    pass


class RucioServiceCreate(ServiceCreate):
    pass


class RucioServiceUpdate(ServiceUpdate):
    pass


class RucioServiceRead(ServiceRead):
    pass


class OneDataServiceQuery(ServiceQuery):
    pass


class OneDataServiceCreate(ServiceCreate):
    pass


class OneDataServiceUpdate(ServiceUpdate):
    pass


class OneDataServiceRead(ServiceRead):
    pass
