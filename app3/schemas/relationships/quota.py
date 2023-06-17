from pydantic import BaseModel, root_validator, validator
from typing import Dict, Optional, Union

from ..utils import (
    QuotaTypeBandwidth,
    QuotaTypeCount,
    QuotaTypeFrequency,
    QuotaTypeMoney,
    QuotaTypeSize,
    QuotaTypeTime,
    QuotaUnit,
)


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
    description: Optional[str] = None
    tot_limit: Optional[float] = None
    instance_limit: Optional[float] = None
    user_limit: Optional[float] = None
    tot_guaranteed: Optional[float] = None
    instance_guaranteed: Optional[float] = None
    user_guaranteed: Optional[float] = None

    @validator("type")
    def get_enum_value(cls, v):
        if v is not None:
            return v.value

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
    tot_guaranteed: float = 0
    instance_guaranteed: float = 0
    user_guaranteed: float = 0


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

    type: Union[
        QuotaTypeBandwidth,
        QuotaTypeCount,
        QuotaTypeFrequency,
        QuotaTypeMoney,
        QuotaTypeSize,
        QuotaTypeTime,
    ]

    @root_validator
    def detect_unit(cls, values) -> Dict:
        quota_type = values["type"]
        if quota_type in [i.value for i in QuotaTypeBandwidth]:
            new_val = QuotaUnit.bandwidth.value
        elif quota_type in [i.value for i in QuotaTypeCount]:
            new_val = None
        elif quota_type in [i.value for i in QuotaTypeFrequency]:
            new_val = QuotaUnit.freq.value
        elif quota_type in [i.value for i in QuotaTypeMoney]:
            new_val = QuotaUnit.money.value
        elif quota_type in [i.value for i in QuotaTypeSize]:
            new_val = QuotaUnit.size.value
        elif quota_type in [i.value for i in QuotaTypeTime]:
            new_val = QuotaUnit.time.value
        else:
            raise TypeError(f"Unknown Quota type: {quota_type}")
        values["unit"] = new_val
        return values


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
    unit: Optional[QuotaUnit] = None

    class Config:
        orm_mode = True
