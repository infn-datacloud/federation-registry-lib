from pydantic import BaseModel
from typing import Optional
from uuid import UUID

from ..utils import ServiceType


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

    name: Optional[ServiceType] = None
    description: Optional[str] = None

    class Config:
        validate_assignment = True


class ServiceUpdate(ServiceBase):
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

    description: str = ""


class ServiceCreate(ServiceUpdate):
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

    name: ServiceType


class Service(ServiceCreate):
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

    uid: UUID

    class Config:
        orm_mode = True
