from enum import Enum
from typing import Dict, Optional, Union
from uuid import UUID
import warnings
from pydantic import BaseModel, root_validator


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

    Class expected as input when performing a REST request.
    It contains the Quota attributes

    Attributes:
        name (str): Quota name.
    """

    name: Union[
        BandwidthQuota,
        CountQuota,
        FrequencyQuota,
        MoneyQuota,
        SizeQuota,
        TimeQuota,
    ]
    description: str = ""
    tot_limit: float
    instance_limit: float
    user_limit: float
    tot_guaranteed: float = 0
    instance_guaranteed: float = 0
    user_guaranteed: float = 0
    unit: Optional[str] = None

    class Config:
        validate_assignment = True


class QuotaCreate(QuotaBase):
    """Quota Actors class

    Class expected as input when performing a REST request.
    It contains the Quota actors.

    Attributes:
        project_id (int): ID of the target Project.
        provider_id (int): ID of the target Provider.
    """

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

    Class expected as output when performing a REST request.
    It contains all the non-sensible data written in the database.

    Attributes:
        id (str): Quota unique ID.
    """

    uid: str

    class Config:
        orm_mode = True
