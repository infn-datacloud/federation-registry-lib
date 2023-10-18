from typing import Optional

from app.models import BaseNode, BaseNodeCreate, BaseNodeRead
from app.query import create_query_model
from app.service.enum import ServiceName, ServiceType
from pydantic import AnyHttpUrl, Extra, Field, validator


class ServiceBase(BaseNode, extra=Extra.allow):
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


class BlockStorageBase(ServiceBase, extra=Extra.ignore):
    """Model derived from ServiceBase to inherit attributes common to all
    services. It adds the basic attributes for BlockStorage services.

    Validation: type value is exactly ServiceType.openstack_nova.
    """

    type: ServiceType = Field(
        default=ServiceType.BLOCK_STORAGE, description="Service type."
    )

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


class BlockStorageServiceCreate(BaseNodeCreate, BlockStorageBase):
    """Model to create a BlockStorage Service.

    Class without id (which is populated by the database). Expected as
    input when performing a POST request.
    """


class BlockStorageServiceUpdate(BlockStorageServiceCreate):
    """Model to update a BlockStorage service.

    Class without id (which is populated by the database). Expected as
    input when performing a PUT request.

    Default to None mandatory attributes.
    """

    endpoint: Optional[AnyHttpUrl] = Field(
        default=None, description="URL of the IaaS service."
    )


class BlockStorageServiceRead(BaseNodeRead, BlockStorageBase):
    """Model to read BlockStorage service data retrieved from DB.

    Class to read data retrieved from the database. Expected as output
    when performing a generic REST request. It contains all the non-
    sensible data written in the database.

    Add the *uid* attribute, which is the item unique identifier in the
    database.
    """


class BlockStorageServiceReadPublic(BaseNodeRead, BlockStorageBase):
    pass


class BlockStorageServiceReadShort(BaseNodeRead, BlockStorageBase):
    pass


BlockStorageServiceQuery = create_query_model(
    "BlockStorageServiceQuery", BlockStorageBase
)


class ComputeBase(ServiceBase, extra=Extra.ignore):
    """Model derived from ServiceBase to inherit attributes common to all
    services. It adds the basic attributes for Compute services.

    Validation: type value is exactly ServiceType.openstack_nova.
    """

    type: ServiceType = Field(default=ServiceType.COMPUTE, description="Service type.")

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


class ComputeServiceCreate(BaseNodeCreate, ComputeBase):
    """Model to create a Compute Service.

    Class without id (which is populated by the database). Expected as
    input when performing a POST request.
    """


class ComputeServiceUpdate(ComputeServiceCreate):
    """Model to update a Compute service.

    Class without id (which is populated by the database). Expected as
    input when performing a PUT request.

    Default to None mandatory attributes.
    """

    endpoint: Optional[AnyHttpUrl] = Field(
        default=None, description="URL of the IaaS service."
    )


class ComputeServiceRead(BaseNodeRead, ComputeBase):
    """Model to read Compute service data retrieved from DB.

    Class to read data retrieved from the database. Expected as output
    when performing a generic REST request. It contains all the non-
    sensible data written in the database.

    Add the *uid* attribute, which is the item unique identifier in the
    database.
    """


class ComputeServiceReadPublic(BaseNodeRead, ComputeBase):
    pass


class ComputeServiceReadShort(BaseNodeRead, ComputeBase):
    pass


ComputeServiceQuery = create_query_model("ComputeServiceQuery", ComputeBase)


class IdentityBase(ServiceBase, extra=Extra.ignore):
    """Model derived from ServiceBase to inherit attributes common to all
    services. It adds the basic attributes for Identity services.

    Validation: type value is exactly ServiceType.openstack_nova.
    """

    type: ServiceType = Field(default=ServiceType.IDENTITY, description="Service type.")

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


class IdentityServiceCreate(BaseNodeCreate, IdentityBase):
    """Model to create a Identity Service.

    Class without id (which is populated by the database). Expected as
    input when performing a POST request.
    """


class IdentityServiceUpdate(IdentityServiceCreate):
    """Model to update a Identity service.

    Class without id (which is populated by the database). Expected as
    input when performing a PUT request.

    Default to None mandatory attributes.
    """

    endpoint: Optional[AnyHttpUrl] = Field(
        default=None, description="URL of the IaaS service."
    )


class IdentityServiceRead(BaseNodeRead, IdentityBase):
    """Model to read Identity service data retrieved from DB.

    Class to read data retrieved from the database. Expected as output
    when performing a generic REST request. It contains all the non-
    sensible data written in the database.

    Add the *uid* attribute, which is the item unique identifier in the
    database.
    """


class IdentityServiceReadPublic(BaseNodeRead, IdentityBase):
    pass


class IdentityServiceReadShort(BaseNodeRead, IdentityBase):
    pass


IdentityServiceQuery = create_query_model("IdentityServiceQuery", IdentityBase)


class NetworkBase(ServiceBase, extra=Extra.ignore):
    """Model derived from ServiceBase to inherit attributes common to all
    services. It adds the basic attributes for Network services.

    Validation: type value is exactly ServiceType.openstack_nova.
    """

    type: ServiceType = Field(default=ServiceType.NETWORK, description="Service type.")

    @validator("name")
    def check_name(cls, v):
        if v != ServiceName.OPENSTACK_NEUTRON:
            raise ValueError(f"Not valid name: {v}")
        return v

    @validator("type")
    def check_type(cls, v):
        if v != ServiceType.NETWORK:
            raise ValueError(f"Not valid type: {v}")
        return v


class NetworkServiceCreate(BaseNodeCreate, NetworkBase):
    """Model to create a Network Service.

    Class without id (which is populated by the database). Expected as
    input when performing a POST request.
    """


class NetworkServiceUpdate(NetworkServiceCreate):
    """Model to update a Network service.

    Class without id (which is populated by the database). Expected as
    input when performing a PUT request.

    Default to None mandatory attributes.
    """

    endpoint: Optional[AnyHttpUrl] = Field(
        default=None, description="URL of the IaaS service."
    )


class NetworkServiceRead(BaseNodeRead, NetworkBase):
    """Model to read Network service data retrieved from DB.

    Class to read data retrieved from the database. Expected as output
    when performing a generic REST request. It contains all the non-
    sensible data written in the database.

    Add the *uid* attribute, which is the item unique identifier in the
    database.
    """


class NetworkServiceReadPublic(BaseNodeRead, NetworkBase):
    pass


class NetworkServiceReadShort(BaseNodeRead, NetworkBase):
    pass


NetworkServiceQuery = create_query_model("NetworkServiceQuery", NetworkBase)
