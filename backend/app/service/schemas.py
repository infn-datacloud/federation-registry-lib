from typing import Optional

from app.models import BaseNode, BaseNodeCreate, BaseNodeRead
from app.query import create_query_model
from app.service.enum import (
    BlockStorageServiceName,
    ComputeServiceName,
    IdentityServiceName,
    NetworkServiceName,
    ServiceType,
)
from pydantic import AnyHttpUrl, Field, validator


class ServiceBase(BaseNode):
    """Model with Service basic attributes."""

    endpoint: AnyHttpUrl = Field(description="URL of the IaaS service.")
    type: ServiceType = Field(description="Service type.")


class BlockStorageServiceBase(ServiceBase):
    """Model derived from ServiceBase to inherit attributes common to all
    services. It adds the basic attributes for BlockStorage services.

    Validation: type value is exactly ServiceType.openstack_nova.
    """

    type: ServiceType = Field(
        default=ServiceType.BLOCK_STORAGE, description="Service type."
    )
    name: BlockStorageServiceName = Field(description="Service name.")

    @validator("type")
    def check_type(cls, v):
        if v != ServiceType.BLOCK_STORAGE:
            raise ValueError(f"Not valid type: {v}")
        return v


class BlockStorageServiceCreate(BaseNodeCreate, BlockStorageServiceBase):
    """Model to create a BlockStorage Service.

    Class without id (which is populated by the database). Expected as
    input when performing a POST request.
    """


class BlockStorageServiceUpdate(BaseNodeCreate, BlockStorageServiceBase):
    """Model to update a BlockStorage service.

    Class without id (which is populated by the database). Expected as
    input when performing a PUT request.

    Default to None mandatory attributes.
    """

    endpoint: Optional[AnyHttpUrl] = Field(
        default=None, description="URL of the IaaS service."
    )
    name: Optional[BlockStorageServiceName] = Field(
        default=None, description="Service name."
    )


class BlockStorageServiceRead(BaseNodeRead, BlockStorageServiceBase):
    """Model to read BlockStorage service data retrieved from DB.

    Class to read data retrieved from the database. Expected as output
    when performing a generic REST request. It contains all the non-
    sensible data written in the database.

    Add the *uid* attribute, which is the item unique identifier in the
    database.
    """


class BlockStorageServiceReadPublic(BaseNodeRead, BlockStorageServiceBase):
    pass


class BlockStorageServiceReadShort(BaseNodeRead, BlockStorageServiceBase):
    pass


BlockStorageServiceQuery = create_query_model(
    "BlockStorageServiceQuery", BlockStorageServiceBase
)


class ComputeServiceBase(ServiceBase):
    """Model derived from ServiceBase to inherit attributes common to all
    services. It adds the basic attributes for Compute services.

    Validation: type value is exactly ServiceType.openstack_nova.
    """

    type: ServiceType = Field(default=ServiceType.COMPUTE, description="Service type.")
    name: ComputeServiceName = Field(description="Service name.")

    @validator("type")
    def check_type(cls, v):
        if v != ServiceType.COMPUTE:
            raise ValueError(f"Not valid type: {v}")
        return v


class ComputeServiceCreate(BaseNodeCreate, ComputeServiceBase):
    """Model to create a Compute Service.

    Class without id (which is populated by the database). Expected as
    input when performing a POST request.
    """


class ComputeServiceUpdate(BaseNodeCreate, ComputeServiceBase):
    """Model to update a Compute service.

    Class without id (which is populated by the database). Expected as
    input when performing a PUT request.

    Default to None mandatory attributes.
    """

    endpoint: Optional[AnyHttpUrl] = Field(
        default=None, description="URL of the IaaS service."
    )
    name: Optional[ComputeServiceName] = Field(
        default=None, description="Service name."
    )


class ComputeServiceRead(BaseNodeRead, ComputeServiceBase):
    """Model to read Compute service data retrieved from DB.

    Class to read data retrieved from the database. Expected as output
    when performing a generic REST request. It contains all the non-
    sensible data written in the database.

    Add the *uid* attribute, which is the item unique identifier in the
    database.
    """


class ComputeServiceReadPublic(BaseNodeRead, ComputeServiceBase):
    pass


class ComputeServiceReadShort(BaseNodeRead, ComputeServiceBase):
    pass


ComputeServiceQuery = create_query_model("ComputeServiceQuery", ComputeServiceBase)


class IdentityServiceBase(ServiceBase):
    """Model derived from ServiceBase to inherit attributes common to all
    services. It adds the basic attributes for Identity services.

    Validation: type value is exactly ServiceType.openstack_nova.
    """

    type: ServiceType = Field(default=ServiceType.IDENTITY, description="Service type.")
    name: IdentityServiceName = Field(description="Service name.")

    @validator("type")
    def check_type(cls, v):
        if v != ServiceType.IDENTITY:
            raise ValueError(f"Not valid type: {v}")
        return v


class IdentityServiceCreate(BaseNodeCreate, IdentityServiceBase):
    """Model to create a Identity Service.

    Class without id (which is populated by the database). Expected as
    input when performing a POST request.
    """


class IdentityServiceUpdate(BaseNodeCreate, IdentityServiceBase):
    """Model to update a Identity service.

    Class without id (which is populated by the database). Expected as
    input when performing a PUT request.

    Default to None mandatory attributes.
    """

    endpoint: Optional[AnyHttpUrl] = Field(
        default=None, description="URL of the IaaS service."
    )
    name: Optional[IdentityServiceName] = Field(
        default=None, description="Service name."
    )


class IdentityServiceRead(BaseNodeRead, IdentityServiceBase):
    """Model to read Identity service data retrieved from DB.

    Class to read data retrieved from the database. Expected as output
    when performing a generic REST request. It contains all the non-
    sensible data written in the database.

    Add the *uid* attribute, which is the item unique identifier in the
    database.
    """


class IdentityServiceReadPublic(BaseNodeRead, IdentityServiceBase):
    pass


class IdentityServiceReadShort(BaseNodeRead, IdentityServiceBase):
    pass


IdentityServiceQuery = create_query_model("IdentityServiceQuery", IdentityServiceBase)


class NetworkServiceBase(ServiceBase):
    """Model derived from ServiceBase to inherit attributes common to all
    services. It adds the basic attributes for Network services.

    Validation: type value is exactly ServiceType.openstack_nova.
    """

    type: ServiceType = Field(default=ServiceType.NETWORK, description="Service type.")
    name: NetworkServiceName = Field(description="Service name.")

    @validator("type")
    def check_type(cls, v):
        if v != ServiceType.NETWORK:
            raise ValueError(f"Not valid type: {v}")
        return v


class NetworkServiceCreate(BaseNodeCreate, NetworkServiceBase):
    """Model to create a Network Service.

    Class without id (which is populated by the database). Expected as
    input when performing a POST request.
    """


class NetworkServiceUpdate(BaseNodeCreate, NetworkServiceBase):
    """Model to update a Network service.

    Class without id (which is populated by the database). Expected as
    input when performing a PUT request.

    Default to None mandatory attributes.
    """

    endpoint: Optional[AnyHttpUrl] = Field(
        default=None, description="URL of the IaaS service."
    )
    name: Optional[NetworkServiceName] = Field(
        default=None, description="Service name."
    )


class NetworkServiceRead(BaseNodeRead, NetworkServiceBase):
    """Model to read Network service data retrieved from DB.

    Class to read data retrieved from the database. Expected as output
    when performing a generic REST request. It contains all the non-
    sensible data written in the database.

    Add the *uid* attribute, which is the item unique identifier in the
    database.
    """


class NetworkServiceReadPublic(BaseNodeRead, NetworkServiceBase):
    pass


class NetworkServiceReadShort(BaseNodeRead, NetworkServiceBase):
    pass


NetworkServiceQuery = create_query_model("NetworkServiceQuery", NetworkServiceBase)
