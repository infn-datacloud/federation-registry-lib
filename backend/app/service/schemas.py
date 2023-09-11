from typing import Optional

from app.models import BaseNodeCreate, BaseNodeRead
from app.query import create_query_model
from app.service.enum import ServiceName, ServiceType
from pydantic import AnyHttpUrl, BaseModel, Extra, Field, validator


class ServiceBase(BaseModel, extra=Extra.allow):
    """Model with Service basic attributes."""

    endpoint: AnyHttpUrl = Field(description="URL of the IaaS service.")
    type: ServiceType = Field(description="Service type.")
    name: ServiceName = Field(description="Service name.")


class ServiceCreate(BaseNodeCreate, ServiceBase):
    """Model to create a Service.

    Class without id (which is populated by the database). Expected as
    input when performing a POST request.
    """


class ServiceUpdate(ServiceCreate):
    """Model to update a Service.

    Class without id (which is populated by the database). Expected as
    input when performing a PUT request.

    Default to None mandatory attributes.
    """

    endpoint: Optional[AnyHttpUrl] = Field(
        default=None, description="URL of the IaaS service."
    )
    type: Optional[ServiceType] = Field(default=None, description="Service type.")
    name: Optional[ServiceName] = Field(default=None, description="Service name.")


class ServiceRead(BaseNodeRead, ServiceBase):
    """Model to read Service data retrieved from DB.

    Class to read data retrieved from the database. Expected as output
    when performing a generic REST request. It contains all the non-
    sensible data written in the database.

    Add the *uid* attribute, which is the item unique identifier in the
    database.
    """


class ServiceReadPublic(BaseNodeRead, ServiceBase):
    pass


class ServiceReadShort(BaseNodeRead, ServiceBase):
    pass


ServiceQuery = create_query_model("ServiceQuery", ServiceBase)


class NovaBase(ServiceBase, extra=Extra.ignore):
    """Model derived from ServiceBase to inherit attributes common to all
    services. It adds the basic attributes for Nova services.

    Validation: type value is exactly ServiceType.openstack_nova.
    """

    @validator("name")
    def check_name(cls, v):
        if v != ServiceName.OPENSTACK_NOVA:
            raise ValueError(f"Not valid name: {v}")
        return v

    @validator("type")
    def check_type(cls, v):
        if v != ServiceType.COMPUTE:
            raise ValueError(f"Not valid type: {v}")
        return v


class NovaServiceCreate(BaseNodeCreate, NovaBase):
    """Model to create a Nova Service.

    Class without id (which is populated by the database). Expected as
    input when performing a POST request.
    """


class NovaServiceUpdate(NovaServiceCreate):
    """Model to update a Nova service.

    Class without id (which is populated by the database). Expected as
    input when performing a PUT request.

    Default to None mandatory attributes.
    """

    endpoint: Optional[AnyHttpUrl] = Field(
        default=None, description="URL of the IaaS service."
    )


class NovaServiceRead(BaseNodeRead, NovaBase):
    """Model to read Nova service data retrieved from DB.

    Class to read data retrieved from the database. Expected as output
    when performing a generic REST request. It contains all the non-
    sensible data written in the database.

    Add the *uid* attribute, which is the item unique identifier in the
    database.
    """


class NovaServiceReadPublic(BaseNodeRead, NovaBase):
    pass


class NovaServiceReadShort(BaseNodeRead, NovaBase):
    pass


NovaServiceQuery = create_query_model("NovaServiceQuery", NovaBase)


class CinderBase(ServiceBase, extra=Extra.ignore):
    """Model derived from ServiceBase to inherit attributes common to all
    services. It adds the basic attributes for Cinder services.

    Validation: type value is exactly ServiceType.openstack_nova.
    """

    @validator("name")
    def check_name(cls, v):
        if v != ServiceName.OPENSTACK_CINDER:
            raise ValueError(f"Not valid name: {v}")
        return v

    @validator("type")
    def check_type(cls, v):
        if v != ServiceType.BLOCK_STORAGE:
            raise ValueError(f"Not valid type: {v}")
        return v


class CinderServiceCreate(BaseNodeCreate, CinderBase):
    """Model to create a Cinder Service.

    Class without id (which is populated by the database). Expected as
    input when performing a POST request.
    """


class CinderServiceUpdate(CinderServiceCreate):
    """Model to update a Cinder service.

    Class without id (which is populated by the database). Expected as
    input when performing a PUT request.

    Default to None mandatory attributes.
    """

    endpoint: Optional[AnyHttpUrl] = Field(
        default=None, description="URL of the IaaS service."
    )


class CinderServiceRead(BaseNodeRead, CinderBase):
    """Model to read Cinder service data retrieved from DB.

    Class to read data retrieved from the database. Expected as output
    when performing a generic REST request. It contains all the non-
    sensible data written in the database.

    Add the *uid* attribute, which is the item unique identifier in the
    database.
    """


class CinderServiceReadPublic(BaseNodeRead, CinderBase):
    pass


class CinderServiceReadShort(BaseNodeRead, CinderBase):
    pass


CinderServiceQuery = create_query_model("CinderServiceQuery", CinderBase)


class KeystoneBase(ServiceBase, extra=Extra.ignore):
    """Model derived from ServiceBase to inherit attributes common to all
    services. It adds the basic attributes for Keystone services.

    Validation: type value is exactly ServiceType.openstack_nova.
    """

    @validator("name")
    def check_name(cls, v):
        if v != ServiceName.OPENSTACK_KEYSTONE:
            raise ValueError(f"Not valid name: {v}")
        return v

    @validator("type")
    def check_type(cls, v):
        if v != ServiceType.IDENTITY:
            raise ValueError(f"Not valid type: {v}")
        return v


class KeystoneServiceCreate(BaseNodeCreate, KeystoneBase):
    """Model to create a Keystone Service.

    Class without id (which is populated by the database). Expected as
    input when performing a POST request.
    """


class KeystoneServiceUpdate(KeystoneServiceCreate):
    """Model to update a Keystone service.

    Class without id (which is populated by the database). Expected as
    input when performing a PUT request.

    Default to None mandatory attributes.
    """

    endpoint: Optional[AnyHttpUrl] = Field(
        default=None, description="URL of the IaaS service."
    )


class KeystoneServiceRead(BaseNodeRead, KeystoneBase):
    """Model to read Keystone service data retrieved from DB.

    Class to read data retrieved from the database. Expected as output
    when performing a generic REST request. It contains all the non-
    sensible data written in the database.

    Add the *uid* attribute, which is the item unique identifier in the
    database.
    """


class KeystoneServiceReadPublic(BaseNodeRead, KeystoneBase):
    pass


class KeystoneServiceReadShort(BaseNodeRead, KeystoneBase):
    pass


KeystoneServiceQuery = create_query_model("KeystoneServiceQuery", KeystoneBase)
