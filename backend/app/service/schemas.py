from pydantic import AnyHttpUrl, BaseModel, Extra, Field, validator
from typing import Optional

from app.models import BaseNodeCreate, BaseNodeRead
from app.query import create_query_model
from app.service.enum import ServiceType


class ServiceBase(BaseModel, extra=Extra.allow):
    """Model with Service basic attributes."""

    endpoint: AnyHttpUrl = Field(description="URL of the IaaS service.")
    type: ServiceType = Field(description="Service type.")


class ServiceCreate(BaseNodeCreate, ServiceBase):
    """Model to create a Service.

    Class without id (which is populated by the database).
    Expected as input when performing a POST request.
    """


class ServiceUpdate(BaseNodeCreate, extra=Extra.allow):
    """Model to update a Service.

    Class without id (which is populated by the database).
    Expected as input when performing a PUT request.

    Default to None mandatory attributes.
    """

    endpoint: Optional[AnyHttpUrl] = Field(
        default=None, description="URL of the IaaS service."
    )
    type: Optional[ServiceType] = Field(
        default=None, description="Service type."
    )


ServiceQuery = create_query_model("ServiceQuery", ServiceBase)


class NovaBase(BaseModel, extra=Extra.ignore):
    """Model derived from Service.
    It contains the basic attributes for Nova services.

    Validation: type value is exactly Nova.
    """

    @validator("type", check_fields=False)
    def check_type(cls, v):
        if v != ServiceType.openstack_nova:
            raise ValueError(f"Not valid type: {v}")
        return v


class NovaServiceQuery(NovaBase, ServiceQuery):
    """Model to add query attributes on Nova services"""


class NovaServiceCreate(NovaBase, BaseNodeCreate, ServiceBase):
    """Model to create a Nova Service.

    Class without id (which is populated by the database).
    Expected as input when performing a POST request.
    """


class NovaServiceUpdate(NovaBase, ServiceUpdate):
    """Model to update a Nova service.

    Class without id (which is populated by the database).
    Expected as input when performing a PUT request.

    Default to None mandatory attributes.
    """


class NovaServiceRead(NovaBase, BaseNodeRead, ServiceBase):
    """Model to read Nova service data retrieved from DB.

    Class to read data retrieved from the database.
    Expected as output when performing a generic REST request.
    It contains all the non-sensible data written in the database.

    Add the *uid* attribute, which is the item unique
    identifier in the database.
    """


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
