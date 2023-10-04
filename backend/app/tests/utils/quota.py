from typing import Optional
from uuid import uuid4

from app.provider.schemas_extended import (
    BlockStorageQuotaCreateExtended,
    ComputeQuotaCreateExtended,
)
from app.quota.models import BlockStorageQuota, ComputeQuota
from app.quota.schemas import QuotaUpdate
from app.tests.utils.utils import (
    random_bool,
    random_lower_string,
    random_non_negative_float,
    random_non_negative_int,
)
from pydantic import UUID4


def create_random_block_storage_quota(
    *, default: bool = False, project: Optional[UUID4] = None
) -> BlockStorageQuotaCreateExtended:
    project = project if project is not None else uuid4()
    kwargs = {}
    if not default:
        kwargs = {
            "description": random_lower_string(),
            "per_user": random_bool(),
            "gigabytes": random_non_negative_int(),
            "per_volume_gigabytes": random_non_negative_int(),
            "volumes": random_non_negative_int(),
        }
    return BlockStorageQuotaCreateExtended(project=project, **kwargs)


def create_random_compute_quota(
    *, default: bool = False, project: Optional[UUID4] = None
) -> ComputeQuotaCreateExtended:
    project = project if project is not None else uuid4()
    kwargs = {}
    if not default:
        kwargs = {
            "description": random_lower_string(),
            "per_user": random_bool(),
            "cores": random_non_negative_int(),
            "fixed_ips": random_non_negative_int(),
            "public_ips": random_non_negative_int(),
            "instances": random_non_negative_int(),
            "ram": random_non_negative_int(),
        }
    return ComputeQuotaCreateExtended(project=project, **kwargs)


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


def validate_block_storage_quota_attrs(
    *, obj_in: BlockStorageQuotaCreateExtended, db_item: BlockStorageQuota
) -> None:
    assert db_item.description == obj_in.description
    assert db_item.type == obj_in.type
    assert db_item.per_user == obj_in.per_user
    assert db_item.gigabytes == obj_in.gigabytes
    assert db_item.per_volume_gigabytes == obj_in.per_volume_gigabytes
    assert db_item.volumes == obj_in.volumes
    if db_item.project:
        assert db_item.project == obj_in.project
    else:
        assert not obj_in.project


def validate_compute_quota_attrs(
    *, obj_in: ComputeQuotaCreateExtended, db_item: ComputeQuota
) -> None:
    assert db_item.description == obj_in.description
    assert db_item.type == obj_in.type
    assert db_item.per_user == obj_in.per_user
    assert db_item.cores == obj_in.cores
    assert db_item.fixed_ips == obj_in.fixed_ips
    assert db_item.public_ips == obj_in.public_ips
    assert db_item.instances == obj_in.instances
    assert db_item.ram == obj_in.ram
    if db_item.project:
        assert db_item.project == obj_in.project
    else:
        assert not obj_in.project
