from .utils import random_lower_string, random_non_negative_float
from ...quota.crud import quota
from ...quota.models import Quota
from ...quota.schemas import QuotaCreate, QuotaUpdate


def create_random_quota() -> Quota:
    description = random_lower_string()
    tot_limit = random_non_negative_float()
    instance_limit = random_non_negative_float()
    user_limit = random_non_negative_float()
    tot_guaranteed = random_non_negative_float()
    instance_guaranteed = random_non_negative_float()
    user_guaranteed = random_non_negative_float()
    item_in = QuotaCreate(
        description=description,
        tot_limit=tot_limit,
        instance_limit=instance_limit,
        user_limit=user_limit,
        tot_guaranteed=tot_guaranteed,
        instance_guaranteed=instance_guaranteed,
        user_guaranteed=user_guaranteed,
    )
    return quota.create(obj_in=item_in)


def create_random_update_quota_data() -> QuotaUpdate:
    description = random_lower_string()
    tot_limit = random_non_negative_float()
    instance_limit = random_non_negative_float()
    user_limit = random_non_negative_float()
    tot_guaranteed = random_non_negative_float()
    instance_guaranteed = random_non_negative_float()
    user_guaranteed = random_non_negative_float()
    return QuotaUpdate(
        description=description,
        tot_limit=tot_limit,
        instance_limit=instance_limit,
        user_limit=user_limit,
        tot_guaranteed=tot_guaranteed,
        instance_guaranteed=instance_guaranteed,
        user_guaranteed=user_guaranteed,
    )
