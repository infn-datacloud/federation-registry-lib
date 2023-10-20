from app.provider.schemas_extended import (
    BlockStorageQuotaCreateExtended,
    ComputeQuotaCreateExtended,
)
from app.quota.models import BlockStorageQuota, ComputeQuota
from app.quota.schemas import BlockStorageQuotaUpdate, ComputeQuotaUpdate
from app.tests.utils.utils import (
    random_bool,
    random_lower_string,
    random_non_negative_int,
)


def create_random_block_storage_quota(
    *, default: bool = False, project: str
) -> BlockStorageQuotaCreateExtended:
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
    *, default: bool = False, project: str
) -> ComputeQuotaCreateExtended:
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


def create_random_block_storage_quota_patch(
    default: bool = False,
) -> BlockStorageQuotaUpdate:
    if default:
        return BlockStorageQuotaUpdate()
    description = random_lower_string()
    per_user = random_bool()
    gigabytes = random_non_negative_int()
    per_volume_gigabytes = random_non_negative_int()
    volumes = random_non_negative_int()
    return BlockStorageQuotaUpdate(
        description=description,
        per_user=per_user,
        gigabytes=gigabytes,
        per_volume_gigabytes=per_volume_gigabytes,
        volumes=volumes,
    )


def create_random_compute_quota_patch(default: bool = False) -> ComputeQuotaUpdate:
    if default:
        return ComputeQuotaUpdate()
    description = random_lower_string()
    per_user = random_bool()
    cores = random_non_negative_int()
    fixed_ips = random_non_negative_int()
    public_ips = random_non_negative_int()
    instances = random_non_negative_int()
    ram = random_non_negative_int()
    return ComputeQuotaUpdate(
        description=description,
        per_user=per_user,
        cores=cores,
        fixed_ips=fixed_ips,
        public_ips=public_ips,
        instances=instances,
        ram=ram,
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
    if db_item.project.single():
        assert db_item.project.single().uuid == str(obj_in.project)
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
    if db_item.project.single():
        assert db_item.project.single().uuid == str(obj_in.project)
    else:
        assert not obj_in.project
