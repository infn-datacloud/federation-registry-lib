"""Pydantic models of the Service supplied by a Provider on a specific Region."""

from typing import Annotated, Literal

from pydantic import AnyHttpUrl, BaseModel, Field

from fedreg.core import BaseNode, BaseNodeRead
from fedreg.service.enum import (
    BlockStorageServiceName,
    ComputeServiceName,
    NetworkServiceName,
    ObjectStoreServiceName,
    ServiceType,
)


class ServiceBase(BaseNode):
    """Model with Service common attributes.

    This model is used also as a public interface.

    Attributes:
    ----------
        description (str): Brief description.
        endpoint (str): URL of the IaaS Service.
    """

    endpoint: Annotated[AnyHttpUrl, Field(description="URL of the IaaS Service.")]


class BlockStorageServiceCreate(ServiceBase):
    """Model with the Block Storage Service public and restricted attributes.

    Model derived from ServiceBase to inherit attributes common to all services.

    Attributes:
    ----------
        description (str): Brief description.
        endpoint (str): URL of the IaaS Service.
        type (str): Service type.
        name (str): Service name. Depends on type.
    """

    type: Annotated[
        Literal[ServiceType.BLOCK_STORAGE],
        Field(
            default=ServiceType.BLOCK_STORAGE, description="Block Storage service type."
        ),
    ]
    name: Annotated[
        BlockStorageServiceName,
        Field(description="Service name/sub-kind. Depends on type."),
    ]


class ComputeServiceCreate(ServiceBase):
    """Model with the Compute Service public and restricted attributes.

    Model derived from ServiceBase to inherit attributes common to all services.

    Attributes:
    ----------
        description (str): Brief description.
        endpoint (str): URL of the IaaS Service.
        type (str): Service type.
        name (str): Service name. Depends on type.
    """

    type: Annotated[
        Literal[ServiceType.COMPUTE],
        Field(default=ServiceType.COMPUTE, description="Compute service type."),
    ]
    name: Annotated[
        ComputeServiceName, Field(description="Service name/sub-kind. Depends on type.")
    ]


class NetworkServiceCreate(ServiceBase):
    """Model with the Network Service public and restricted attributes.

    Model derived from ServiceBase to inherit attributes common to all services.

    Attributes:
    ----------
        description (str): Brief description.
        endpoint (str): URL of the IaaS Service.
        type (str): Service type.
        name (str): Service name. Depends on type.
    """

    type: Annotated[
        Literal[ServiceType.NETWORK],
        Field(default=ServiceType.NETWORK, description="Network service type."),
    ]
    name: Annotated[
        NetworkServiceName, Field(description="Service name/sub-kind. Depends on type.")
    ]


class ObjectStoreServiceCreate(ServiceBase):
    """Model with the Object Storage Service public and restricted attributes.

    Model derived from ServiceBase to inherit attributes common to all services.

    Attributes:
    ----------
        description (str): Brief description.
        endpoint (str): URL of the IaaS Service.
        type (str): Service type.
        name (str): Service name. Depends on type.
    """

    type: Annotated[
        Literal[ServiceType.OBJECT_STORE],
        Field(
            default=ServiceType.OBJECT_STORE, description="Object Storage service type."
        ),
    ]
    name: Annotated[
        ObjectStoreServiceName,
        Field(description="Service name/sub-kind. Depends on type."),
    ]


class ServiceRead(BaseNodeRead, ServiceBase):
    """Represents a read-only view of a service node with type and name.

    Inherits from:
        BaseNodeRead: Base class for node read operations.
        ServiceBase: Base class for service-related attributes.

    Attributes:
        type (ServiceType): The type of the object storage service.
        name (BlockStorageServiceName | ComputeServiceName | NetworkServiceName | ObjectStoreServiceName):
            The specific name or sub-kind of the service, which depends on the service
            type.
    """  # noqa: E501

    type: Annotated[ServiceType, Field(description="Object Storage service type.")]
    name: Annotated[
        BlockStorageServiceName
        | ComputeServiceName
        | NetworkServiceName
        | ObjectStoreServiceName,
        Field(description="Service name/sub-kind. Depends on type."),
    ]


class ServiceQuery(BaseModel):
    """ServiceQuery model for querying IaaS services.

    Attributes:
        endpoint (str | None): URL of the IaaS Service.
        type (str | None): Service type.
        name (str | None): Service name or sub-kind, depending on the service type.
    """

    endpoint: Annotated[
        str | None, Field(default=None, description="URL of the IaaS Service.")
    ]
    type: Annotated[str | None, Field(default=None, description="Service type.")]
    name: Annotated[
        str | None,
        Field(default=None, description="Service name/sub-kind. Depends on type."),
    ]
