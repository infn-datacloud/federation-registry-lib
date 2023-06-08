from enum import Enum
from pydantic import BaseModel, root_validator
from typing import Dict, Optional, Union
import warnings


class BandwidthQuota(Enum):
    upload_bandwidth: str = "Upload Bandwidth"
    download_bandwidth: str = "Download Bandwidth"


class CountQuota(Enum):
    num_cpus: str = "Num CPUs"
    public_ip: str = "Public IPs"


class FrequencyQuota(Enum):
    cpu_frequency: str = "CPU frequency"


class MoneyQuota(Enum):
    cost: str = "Cost"


class SizeQuota(Enum):
    mem_size: str = "RAM Memory Size"
    disk_size: str = "Disk Size"
    upload_aggregated: str = "Upload Aggregated"
    download_aggregated: str = "Download Aggregated"


class TimeQuota(Enum):
    computing_time: str = "Compute Time"


class Unit(Enum):
    bandwidth = "Mbps"
    freq = "Hz"
    money = "€"
    size = "MB"
    time = "h"


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
            BandwidthQuota,
            CountQuota,
            FrequencyQuota,
            MoneyQuota,
            SizeQuota,
            TimeQuota,
        ]
    ] = None
    description: str = ""
    tot_limit: Optional[float] = None
    instance_limit: Optional[float] = None
    user_limit: Optional[float] = None
    tot_guaranteed: float = 0
    instance_guaranteed: float = 0
    user_guaranteed: float = 0
    unit: Optional[str] = None

    class Config:
        validate_assignment = True


class QuotaCreate(QuotaBase):
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
        BandwidthQuota,
        CountQuota,
        FrequencyQuota,
        MoneyQuota,
        SizeQuota,
        TimeQuota,
    ]
    tot_limit: float
    instance_limit: float
    user_limit: float

    @root_validator
    def detect_unit(cls, values) -> Dict:
        quota_type = values["name"]
        if type(quota_type) is BandwidthQuota:
            new_val = Unit.bandwidth
        elif type(quota_type) is CountQuota:
            new_val = None
        elif type(quota_type) is FrequencyQuota:
            new_val = Unit.freq
        elif type(quota_type) is MoneyQuota:
            new_val = Unit.money
        elif type(quota_type) is SizeQuota:
            new_val = Unit.size
        elif type(quota_type) is TimeQuota:
            new_val = Unit.time
        else:
            raise TypeError(f"Unknown Quota type: {quota_type}")

        if values["unit"] is not None:
            warnings.warn(f"Overriding unit with new value: {new_val}")

        values["unit"] = new_val
        return values


class Quota(QuotaBase):
    """Quota Base class

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
