from pydantic import BaseModel, Field, validator
from typing import Optional

from .quota_type import QuotaType, QuotaTypeCreate
from .service import Service, ServiceCreate
from ..utils import get_single_node_from_rel


class QuotaBase(BaseModel):
    """Quota Base class

    Class without id (which is populated by the database).
    Expected as input when performing a PATCH REST request.

    Attributes:
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

    description: Optional[str] = None
    tot_limit: Optional[float] = Field(ge=0, default=None)
    instance_limit: Optional[float] = Field(ge=0, default=None)
    user_limit: Optional[float] = Field(ge=0, default=None)
    tot_guaranteed: Optional[float] = Field(ge=0, default=None)
    instance_guaranteed: Optional[float] = Field(ge=0, default=None)
    user_guaranteed: Optional[float] = Field(ge=0, default=None)

    class Config:
        validate_assignment = True


class QuotaUpdate(QuotaBase):
    """Quota Base class

    Class without id (which is populated by the database).
    Expected as input when performing a PATCH REST request.

    Attributes:
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

    description: str = ""
    tot_guaranteed: float = Field(ge=0, default=0)
    instance_guaranteed: float = Field(ge=0, default=0)
    user_guaranteed: float = Field(ge=0, default=0)
    type: Optional[QuotaTypeCreate] = None
    service: Optional[ServiceCreate] = None


class QuotaCreate(QuotaUpdate):
    """Quota Create class

    Class without id (which is populated by the database).
    Expected as input when performing a POST REST request.


    Attributes:
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

    type: QuotaTypeCreate
    service: ServiceCreate


class Quota(QuotaCreate):
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

    uid: str
    type: QuotaType
    service: Service

    _get_single_type = validator("type", pre=True, allow_reuse=True)(
        get_single_node_from_rel
    )
    _get_single_service = validator("service", pre=True, allow_reuse=True)(
        get_single_node_from_rel
    )

    class Config:
        orm_mode = True
