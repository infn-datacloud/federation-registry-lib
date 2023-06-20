from pydantic import BaseModel, Field, validator
from typing import List, Optional
from uuid import UUID

from .quota_type import QuotaType, QuotaTypeCreate
from ..utils import (
    get_all_nodes_from_rel,
    get_enum_value,
    ServiceType as SrvType,
)


class ServiceTypeBase(BaseModel):
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

    name: Optional[SrvType] = None
    description: Optional[str] = None

    _get_name = validator("name", allow_reuse=True)(get_enum_value)

    class Config:
        validate_assignment = True


class ServiceTypeUpdate(ServiceTypeBase):
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
    quota_types: List[QuotaTypeCreate] = Field(default_factory=list)


class ServiceTypeCreate(ServiceTypeUpdate):
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

    name: SrvType
    quota_types: List[QuotaTypeCreate]


class ServiceType(ServiceTypeCreate):
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
    quota_types: List[QuotaType]

    _get_all_quota_types = validator(
        "quota_types", pre=True, allow_reuse=True
    )(get_all_nodes_from_rel)

    class Config:
        orm_mode = True
