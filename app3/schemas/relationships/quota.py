from pydantic import BaseModel, root_validator
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
        name (str): Quota name (type).
        description (str): Brief description.
        unit (str | None): Measurement unit derived from the
            quota name/type.
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

    name: Optional[
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

    class Config:
        validate_assignment = True


class QuotaUpdate(QuotaBase):
    """Quota Base class

    Class without id (which is populated by the database).
    Expected as input when performing a PATCH REST request.

    Attributes:
        name (str): Quota name (type).
        description (str): Brief description.
        unit (str | None): Measurement unit derived from the
            quota name/type.
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
        name (str): Quota name (type).
        description (str): Brief description.
        unit (str | None): Measurement unit derived from the
            quota name/type.
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

    name: Union[
        QuotaTypeBandwidth,
        QuotaTypeCount,
        QuotaTypeFrequency,
        QuotaTypeMoney,
        QuotaTypeSize,
        QuotaTypeTime,
    ]
    tot_limit: float
    instance_limit: float
    user_limit: float
    unit: Optional[str] = None

    @root_validator
    def detect_unit(cls, values) -> Dict:
        quota_type = values["name"]
        if type(quota_type) is QuotaTypeBandwidth:
            new_val = QuotaUnit.bandwidth
        elif type(quota_type) is QuotaTypeCount:
            new_val = None
        elif type(quota_type) is QuotaTypeFrequency:
            new_val = QuotaUnit.freq
        elif type(quota_type) is QuotaTypeMoney:
            new_val = QuotaUnit.money
        elif type(quota_type) is QuotaTypeSize:
            new_val = QuotaUnit.size
        elif type(quota_type) is QuotaTypeTime:
            new_val = QuotaUnit.time
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
        name (str): Quota name (type).
        description (str): Brief description.
        unit (str | None): Measurement unit derived from the
            quota name/type.
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

    class Config:
        orm_mode = True
