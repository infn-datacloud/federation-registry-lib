from enum import Enum
from pydantic import BaseModel, Field, root_validator
from typing import Dict, List, Optional, Union
import warnings


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

    Class without id (which is populated by the database).
    Expected as input when performing a PATCH REST request.

    Attributes:
        name (str): Service name (type).
        description (str): Brief description.
        resource_type (str): Resource type.
        endpoint (str): URL pointing to this service
        iam_enabled (bool): IAM enabled for this service.
        is_public (bool): Public Service or not.
        public_ip_assignable (bool): It is possible to
            assign a public IP to this service.
        volume_types (list of str): TODO
    """

    name: Optional[
        Union[ComputeServiceType, NetworkServiceType, StorageServiceType]
    ] = None
    description: str = ""
    resource_type: Optional[ResourceType] = None
    endpoint: Optional[str] = None
    iam_enabled: bool = False
    is_public: bool = False
    public_ip_assignable: bool = False
    volume_types: List[str] = Field(default_factory=list)

    class Config:
        validate_assignment = True


class ServiceCreate(ServiceBase):
    """Service Create class

    Class without id (which is populated by the database).
    Expected as input when performing a POST REST request.

    Attributes:
        name (str): Service name (type).
        description (str): Brief description.
        resource_type (str): Resource type.
        endpoint (str): URL pointing to this service
        iam_enabled (bool): IAM enabled for this service.
        is_public (bool): Public Service or not.
        public_ip_assignable (bool): It is possible to
            assign a public IP to this service.
        volume_types (list of str): TODO
    """

    name: Union[ComputeServiceType, NetworkServiceType, StorageServiceType]
    resource_type: ResourceType
    endpoint: str

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

    Class retrieved from the database
    expected as output when performing a REST request.
    It contains all the non-sensible data written
    in the database.

    Attributes:
        uid (uuid): Service unique ID.
        name (str): Service name (type).
        description (str): Brief description.
        resource_type (str): Resource type.
        endpoint (str): URL pointing to this service
        iam_enabled (bool): IAM enabled for this service.
        is_public (bool): Public Service or not.
        public_ip_assignable (bool): It is possible to
            assign a public IP to this service.
        volume_types (list of str): TODO
    """

    uid: str

    class Config:
        orm_mode = True
