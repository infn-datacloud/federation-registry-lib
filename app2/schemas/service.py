from enum import Enum
from uuid import UUID
import warnings
from pydantic import BaseModel, Field, root_validator
from typing import Dict, List, Optional, Union

from .identity_provider import IdentityProvider


class ComputeServiceType(Enum):
    open_stack_nova: str = "org.openstack.nova"
    mesos: str = "eu.indigo-datacloud.mesos"
    chronos: str = "eu.indigo-datacloud.chronos"
    marathon: str = "eu.indigo-datacloud.marathon"
    kubernetes: str = "eu.deep.kubernetes"


class NetworkServiceType(Enum):
    pass


class StorageServiceType(Enum):
    rucio: str = "eu.egi.storage-element"
    onedata: str = "eu.egi.cloud.storage-management.oneprovider"


class ResourceType(Enum):
    """Possible resource types"""

    Compute: str = "Compute"
    Storage: str = "Storage"
    Network: str = "Network"


class ServiceBase(BaseModel):
    """Service Base class

    Class without id which is populated by the database.

    Attributes:
        name (str): Service name.
        site_name (str): Service site name.
        hostname (str): Service hostname.
        endpoint (str): Service endpoint.
        identity_provider_protocol (str): Identity Provider protocol.
        iam_enabled (str): Authentication through IAM enabled.
    """

    name: Union[ComputeServiceType, NetworkServiceType, StorageServiceType]
    description: str = ""
    resource_type: Optional[ResourceType]
    site_name: str
    hostname: str
    endpoint: str
    identity_provider_protocol: str
    iam_enabled: bool
    # identity_providers: List[IdentityProvider] = Field(default_factory=list)

    class Config:
        validate_assignment = True


class ServiceCreate(ServiceBase):
    """Service Create class

    Class expected as input when performing a REST request.

    Attributes:
        name (str): Service name.
        site_name (str): Service site name.
        hostname (str): Service hostname.
        endpoint (str): Service endpoint.
        identity_provider_protocol (str): Identity Provider protocol.
        iam_enabled (str): Authentication through IAM enabled.
    """

    @root_validator
    def detect_resource_type(cls, values) -> Dict:
        srv_type = values["name"]
        if type(srv_type) is ComputeServiceType:
            new_val = ResourceType.Compute
        elif type(srv_type) is NetworkServiceType:
            new_val = ResourceType.Network
        elif type(srv_type) is StorageServiceType:
            new_val = ResourceType.Storage
        else:
            raise TypeError("Unknown Service type: {srv_type}")

        if values["resource_type"] is not None:
            warnings.warn(
                f"Overriding resource_type with new value: {new_val}"
            )
        values["resource_type"] = new_val
        return values


class Service(ServiceBase):
    """Service Base class

    Class expected as output when performing a REST request.
    It contains all the non-sensible data written in the database.

    Attributes:
        id (str): Service unique ID.
        name (str): Service name.
        site_name (str): Service site name.
        hostname (str): Service hostname.
        endpoint (str): Service endpoint.
        identity_provider_protocol (str): Identity Provider protocol.
        iam_enabled (str): Authentication through IAM enabled.
    """

    id: UUID

    class Config:
        orm_mode = True
