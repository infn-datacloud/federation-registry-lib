from neomodel import One
from pydantic import validator

from .schemas import Quota, QuotaCreate, QuotaUpdate
from ..quota_type.schemas import QuotaType, QuotaTypeCreate
from ..service.schemas import Service, ServiceCreate
from ..validators import get_single_node_from_rel


class QuotaCreateExtended(QuotaCreate):
    type: QuotaTypeCreate
    service: ServiceCreate


class QuotaUpdateExtended(QuotaUpdate):
    """Quota Update Model class.

    Class without id (which is populated by the database).
    Expected as input when performing a PATCH request.

    Attributes:
        description (str): Brief description.
        tot_limit (float | None): The max quantity of a resource to
            be granted to the user group in total.
        instance_limit (float | None): The max quantity of a resource
            to be granted to each VM/Container instance.
        user_limit (float | None): The max quantity of a resource to
            be granted to user.
        tot_guaranteed (float): The guaranteed quantity of a
            resource to be granted to the user group in total.
        instance_guaranteed (float): The guaranteed quantity
            of a resource to be granted to each VM/Container
            instance.
        user_guaranteed (float): The guaranteed quantity
            of a resource to be granted to user.
        type (QuotaType | None): Quota type.
        service (Service | None): Service where this quota applies.
    """

    type: QuotaType
    service: Service


class QuotaExtended(Quota):
    """Quota class

    Class retrieved from the database
    expected as output when performing a REST request.
    It contains all the non-sensible data written
    in the database.

    Attributes:
        uid (uuid): Quota unique ID.
        type (str): Quota type (type).
        description (str): Brief description.
        unit (str | None): Measurement unit derived from the
            quota type/type.
        tot_limit (float | None): The max quantity of a resource to
            be granted to the user group in total.
        instance_limit (float | None): The max quantity of a resource
            to be granted to each VM/Container instance.
        user_limit (float | None): The max quantity of a resource to
            be granted to user.
        tot_guaranteed (float): The guaranteed quantity of a
            resource to be granted to the user group in total.
        instance_guaranteed (float): The guaranteed quantity
            of a resource to be granted to each VM/Container
            instance.
        user_guaranteed (float): The guaranteed quantity
            of a resource to be granted to user.
    """

    type: QuotaType
    service: Service

    @validator("type", pre=True)
    def get_single_type(cls, v: One) -> QuotaType:
        return get_single_node_from_rel(v)

    @validator("service", pre=True)
    def get_single_srv(cls, v: One) -> Service:
        return get_single_node_from_rel(v)
