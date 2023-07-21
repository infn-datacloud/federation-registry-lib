from pydantic import BaseModel, Extra, validator
from typing import Optional, Union

from app.quota.enum import (
    QuotaTypeBandwidth,
    QuotaTypeCount,
    QuotaTypeFrequency,
    QuotaTypeMoney,
    QuotaTypeSize,
    QuotaTypeTime,
)
from app.models import BaseNodeCreate, BaseNodeQuery, BaseNodeRead


class QuotaBase(BaseModel, extra=Extra.allow):
    type: Union[
        QuotaTypeBandwidth,
        QuotaTypeCount,
        QuotaTypeFrequency,
        QuotaTypeMoney,
        QuotaTypeSize,
        QuotaTypeTime,
    ]


class QuotaQuery(BaseNodeQuery, QuotaBase):
    """Quota Query Model class.

    Attributes:
        description (str | None): Brief description.
        tot_limit (float | None): The max quantity of a resource to
            be granted to the user group in total.
        instance_limit (float | None): The max quantity of a resource
            to be granted to each VM/Container instance.
        user_limit (float | None): The max quantity of a resource to
            be granted to user.
        tot_guaranteed (float| None): The guaranteed quantity of a
            resource to be granted to the user group in total.
        instance_guaranteed (float | None): The guaranteed quantity
            of a resource to be granted to each VM/Container
            instance.
        user_guaranteed (float | None): The guaranteed quantity
            of a resource to be granted to user.
    """

    type: Optional[
        Union[
            QuotaTypeBandwidth,
            QuotaTypeCount,
            QuotaTypeFrequency,
            QuotaTypeMoney,
            QuotaTypeSize,
            QuotaTypeTime,
        ]
    ] = None
    # tot_limit: Optional[float] = Field(ge=0, default=None)
    # instance_limit: Optional[float] = Field(ge=0, default=None)
    # user_limit: Optional[float] = Field(ge=0, default=None)
    # tot_guaranteed: Optional[float] = Field(ge=0, default=None)
    # instance_guaranteed: Optional[float] = Field(ge=0, default=None)
    # user_guaranteed: Optional[float] = Field(ge=0, default=None)


class QuotaCreate(BaseNodeCreate, QuotaBase):
    """Quota Create Model class.

    Class without id (which is populated by the database).
    Expected as input when performing a PUT or POST request.

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
        type (QuotaType): Quota type.
        service (Service): Service where this quota applies.
    """

    # tot_limit: Optional[float] = Field(ge=0, default=None)
    # instance_limit: Optional[float] = Field(ge=0, default=None)
    # user_limit: Optional[float] = Field(ge=0, default=None)
    # tot_guaranteed: float = Field(ge=0, default=0)
    # instance_guaranteed: float = Field(ge=0, default=0)
    # user_guaranteed: float = Field(ge=0, default=0)


class QuotaUpdate(BaseNodeCreate, extra=Extra.allow):
    """Quota Update Model class.

    Class without id (which is populated by the database).
    Expected as input when performing a PUT request.

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


class QuotaRead(BaseNodeRead, QuotaBase):
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


class NumCPUQuotaBase(BaseModel, extra=Extra.ignore):
    @validator("type", check_fields=False)
    def check_type(cls, v):
        if v != QuotaTypeCount.num_cpu:
            raise ValueError(f"Not valid type: {v}")
        return v


class NumCPUQuotaCreate(NumCPUQuotaBase, BaseNodeCreate, QuotaBase):
    pass


class NumCPUQuotaUpdate(NumCPUQuotaBase, QuotaUpdate):
    pass


class NumCPUQuotaRead(NumCPUQuotaBase, BaseNodeCreate, QuotaRead):
    pass


class RAMQuotaBase(BaseModel, extra=Extra.ignore):
    @validator("type", check_fields=False)
    def check_type(cls, v):
        if v != QuotaTypeSize.mem_size:
            raise ValueError(f"Not valid type: {v}")
        return v


class RAMQuotaCreate(RAMQuotaBase, BaseNodeCreate, QuotaBase):
    pass


class RAMQuotaUpdate(RAMQuotaBase, QuotaUpdate):
    pass


class RAMQuotaRead(RAMQuotaBase, BaseNodeCreate, QuotaRead):
    pass
