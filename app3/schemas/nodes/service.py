from pydantic import AnyUrl, validator
from typing import Optional

from .service_type import ServiceType, ServiceTypePatch
from ..utils.base_model import BaseNodeCreate, BaseNodeQuery, BaseNodeRead
from ..utils.validators import get_single_node_from_rel


class ServiceQuery(BaseNodeQuery):
    """Service Query Model class.

    Attributes:
        description (str | None): Brief description.
        endpoint (str | None): URL pointing to this service
    """

    endpoint: Optional[AnyUrl] = None


class ServicePatch(BaseNodeCreate):
    """Service Patch Model class.

    Class without id (which is populated by the database).
    Expected as input when performing a PATCH, PUT or POST request.

    Attributes:
        description (str): Brief description.
        endpoint (str | None): URL pointing to this service
        type (ServiceTypePatch | None): Service type.
    """

    type: Optional[ServiceTypePatch] = None


class ServiceCreate(ServicePatch):
    """Service Create Model class.

    Class without id (which is populated by the database).
    Expected as input when performing a PATCH, PUT or POST request.

    Attributes:
        description (str): Brief description.
        endpoint (str): URL pointing to this service
        type (ServiceTypePatch): Service type.
    """

    endpoint: AnyUrl
    type: ServiceTypePatch


class Service(ServiceCreate, BaseNodeRead):
    """Service class.

    Class retrieved from the database.
    Expected as output when performing a REST request.
    It contains all the non-sensible data written
    in the database.

    Attributes:
        uid (uuid): Unique ID.
        description (str): Brief description.
        endpoint (str): URL pointing to this service
        type (ServiceType): Service type.
    """

    type: ServiceType

    _get_single_service_type = validator("type", pre=True, allow_reuse=True)(
        get_single_node_from_rel
    )
