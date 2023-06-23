from typing import Optional, Union

from .enum import (
    QuotaTypeBandwidth,
    QuotaTypeCount,
    QuotaTypeFrequency,
    QuotaTypeMoney,
    QuotaTypeSize,
    QuotaTypeTime,
    QuotaUnit,
)
from ..models import BaseNodeCreate, BaseNodeQuery, BaseNodeRead


class QuotaTypeQuery(BaseNodeQuery):
    """Quota Query Model class.

    Attributes:
        description (str | None): Brief description.
        name (str | None): Type unique name.
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


class QuotaTypePatch(BaseNodeCreate):
    """Quota Patch Model class.

    Class without id (which is populated by the database).
    Expected as input when performing a PATCH request.

    Attributes:
        description (str): Brief description.
        name (str | None): Type unique name.
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

    # @root_validator TODO
    # def detect_unit(cls, values: Dict) -> Dict:
    #    quota_name = values.get("name")
    #    if quota_name is None:
    #        return values
    #
    #    if quota_name in [i for i in QuotaTypeBandwidth]:
    #        new_val = QuotaUnit.bandwidth.value
    #    elif quota_name in [i for i in QuotaTypeCount]:
    #        new_val = None
    #    elif quota_name in [i for i in QuotaTypeFrequency]:
    #        new_val = QuotaUnit.freq.value
    #    elif quota_name in [i for i in QuotaTypeMoney]:
    #        new_val = QuotaUnit.money.value
    #    elif quota_name in [i for i in QuotaTypeSize]:
    #        new_val = QuotaUnit.size.value
    #    elif quota_name in [i for i in QuotaTypeTime]:
    #        new_val = QuotaUnit.time.value
    #    else:
    #        raise TypeError(f"Unknown Quota type: {quota_name}")
    #    values["unit"] = new_val
    #    return values
    #


class QuotaTypeCreate(QuotaTypePatch):
    """Quota Create Model class.

    Class without id (which is populated by the database).
    Expected as input when performing a PUT or POST request.

    Attributes:
        description (str): Brief description.
        name (str): Type unique name.
    """

    name: Union[
        QuotaTypeBandwidth,
        QuotaTypeCount,
        QuotaTypeFrequency,
        QuotaTypeMoney,
        QuotaTypeSize,
        QuotaTypeTime,
    ]


class QuotaType(QuotaTypeCreate, BaseNodeRead):
    """Quota class.

    Class retrieved from the database.
    Expected as output when performing a REST request.
    It contains all the non-sensible data written
    in the database.

    Attributes:
        uid (uuid): Unique ID.
        description (str): Brief description.
        unit (str | None): Measurement unit derived from the
            quota type/type.
    """

    unit: Optional[QuotaUnit] = None
