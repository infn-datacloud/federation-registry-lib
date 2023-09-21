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
    region: Optional[str] = Field(
        default=None,
        description="When dealing with openstack service region is essential",
    )


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


class NetworkBase(ServiceBase, extra=Extra.ignore):
    """Model derived from ServiceBase to inherit attributes common to all
    services. It adds the basic attributes for Network services.

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
