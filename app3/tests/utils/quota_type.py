from random import choice

from .utils import random_lower_string
from ...quota_type.crud import quota_type
from ...quota_type.enum import (
    QuotaTypeBandwidth,
    QuotaTypeCount,
    QuotaTypeFrequency,
    QuotaTypeMoney,
    QuotaTypeSize,
    QuotaTypeTime,
)
from ...quota_type.models import QuotaType
from ...quota_type.schemas import QuotaTypeCreate, QuotaTypeUpdate


def create_random_quota_type() -> QuotaType:
    description = random_lower_string()
    name = random_name()
    item_in = QuotaTypeCreate(name=name, description=description)
    return quota_type.create(obj_in=item_in)


def create_random_update_quota_type_data() -> QuotaTypeUpdate:
    description = random_lower_string()
    name = random_name()
    return QuotaTypeUpdate(name=name, description=description)


def random_name() -> str:
    values = [i.value for i in QuotaTypeBandwidth]
    values += [i.value for i in QuotaTypeCount]
    values += [i.value for i in QuotaTypeFrequency]
    values += [i.value for i in QuotaTypeMoney]
    values += [i.value for i in QuotaTypeSize]
    values += [i.value for i in QuotaTypeTime]
    return choice(values)
