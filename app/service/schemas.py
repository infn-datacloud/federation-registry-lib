from pydantic import AnyHttpUrl, BaseModel, Extra, validator

from app.models import BaseNodeCreate, BaseNodeRead
from app.query import create_query_model
from app.service.enum import ServiceType


class ServiceBase(BaseModel, extra=Extra.allow):
    """Service Create Model class.

    Class without id (which is populated by the database).
    Expected as input when performing a PUT, PUT or POST request.

    Attributes:
        description (str): Brief description.
        endpoint (str): URL pointing to this service
        type (ServiceTypeUpdate): Service type.
    """

    endpoint: AnyHttpUrl
    type: ServiceType


class ServiceCreate(BaseNodeCreate, ServiceBase):
    """Service Create Model class.

    Class without id (which is populated by the database).
    Expected as input when performing a PUT, PUT or POST request.

    Attributes:
        description (str): Brief description.
        endpoint (str): URL pointing to this service
        type (ServiceTypeUpdate): Service type.
    """


class ServiceUpdate(ServiceCreate):
    """Service Create Model class.

    Class without id (which is populated by the database).
    Expected as input when performing a PUT, PUT or POST request.

    Attributes:
        description (str): Brief description.
        endpoint (str): URL pointing to this service
        type (ServiceTypeUpdate): Service type.
    """


ServiceQuery = create_query_model("ServiceQuery", ServiceBase)


class NovaBase(BaseModel, extra=Extra.ignore):
    @validator("type", check_fields=False)
    def check_type(cls, v):
        if v != ServiceType.openstack_nova:
            raise ValueError(f"Not valid type: {v}")
        return v


class NovaServiceQuery(NovaBase, ServiceQuery):
    pass


class NovaServiceCreate(NovaBase, BaseNodeCreate, ServiceBase):
    pass


class NovaServiceUpdate(NovaBase, ServiceUpdate):
    pass


class NovaServiceRead(NovaBase, BaseNodeRead, ServiceBase):
    """Service class.

    Class retrieved from the database.
    Expected as output when performing a REST request.
    It contains all the non-sensible data written
    in the database.

    Attributes:
        uid (uuid): Unique ID.
        description (str): Brief description.
        endpoint (str): URL pointing to this service
        type (ServiceType): Service type equals to org.openstack.nova
    """

    pass


class MesosBase(BaseModel, extra=Extra.ignore):
    @validator("type", check_fields=False)
    def check_type(cls, v):
        if v != ServiceType.mesos:
            raise ValueError(f"Not valid type: {v}")
        return v


class MesosServiceQuery(MesosBase, ServiceQuery):
    pass


class MesosServiceCreate(MesosBase, BaseNodeCreate, ServiceBase):
    pass


class MesosServiceUpdate(MesosBase, ServiceUpdate):
    pass


class MesosServiceRead(MesosBase, BaseNodeRead, ServiceBase):
    pass


class ChronosBase(BaseModel, extra=Extra.ignore):
    @validator("type", check_fields=False)
    def check_type(cls, v):
        if v != ServiceType.chronos:
            raise ValueError(f"Not valid type: {v}")
        return v


class ChronosServiceQuery(ChronosBase, ServiceQuery):
    pass


class ChronosServiceCreate(ChronosBase, BaseNodeCreate, ServiceBase):
    pass


class ChronosServiceUpdate(ChronosBase, ServiceUpdate):
    pass


class ChronosServiceRead(ChronosBase, BaseNodeRead, ServiceBase):
    pass


class MarathonBase(BaseModel, extra=Extra.ignore):
    @validator("type", check_fields=False)
    def check_type(cls, v):
        if v != ServiceType.marathon:
            raise ValueError(f"Not valid type: {v}")
        return v


class MarathonServiceQuery(MarathonBase, ServiceQuery):
    pass


class MarathonServiceCreate(MarathonBase, BaseNodeCreate, ServiceBase):
    pass


class MarathonServiceUpdate(MarathonBase, ServiceUpdate):
    pass


class MarathonServiceRead(MarathonBase, BaseNodeRead, ServiceBase):
    pass


class KubernetesBase(BaseModel, extra=Extra.ignore):
    @validator("type", check_fields=False)
    def check_type(cls, v):
        if v != ServiceType.kubernetes:
            raise ValueError(f"Not valid type: {v}")
        return v


class KubernetesServiceQuery(KubernetesBase, ServiceQuery):
    pass


class KubernetesServiceCreate(KubernetesBase, BaseNodeCreate, ServiceBase):
    pass


class KubernetesServiceUpdate(KubernetesBase, ServiceUpdate):
    pass


class KubernetesServiceRead(KubernetesBase, BaseNodeRead, ServiceBase):
    pass


class RucioBase(BaseModel, extra=Extra.ignore):
    @validator("type", check_fields=False)
    def check_type(cls, v):
        if v != ServiceType.rucio:
            raise ValueError(f"Not valid type: {v}")
        return v


class RucioServiceQuery(RucioBase, ServiceQuery):
    pass


class RucioServiceCreate(RucioBase, BaseNodeCreate, ServiceBase):
    pass


class RucioServiceUpdate(RucioBase, ServiceUpdate):
    pass


class RucioServiceRead(RucioBase, BaseNodeRead, ServiceBase):
    pass


class OneDataBase(BaseModel, extra=Extra.ignore):
    @validator("type", check_fields=False)
    def check_type(cls, v):
        if v != ServiceType.onedata:
            raise ValueError(f"Not valid type: {v}")
        return v


class OneDataServiceQuery(OneDataBase, ServiceQuery):
    pass


class OneDataServiceCreate(OneDataBase, BaseNodeCreate, ServiceBase):
    pass


class OneDataServiceUpdate(OneDataBase, ServiceUpdate):
    pass


class OneDataServiceRead(OneDataBase, BaseNodeRead, ServiceBase):
    pass
