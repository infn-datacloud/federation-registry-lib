from typing import Union

from app.provider.schemas_extended import BlockStorageQuotaCreateExtended
from app.quota.models import BlockStorageQuota
from app.quota.schemas import (
    BlockStorageQuotaBase,
    BlockStorageQuotaRead,
    BlockStorageQuotaReadPublic,
    BlockStorageQuotaReadShort,
    BlockStorageQuotaUpdate,
)
from app.quota.schemas_extended import (
    BlockStorageQuotaReadExtended,
    BlockStorageQuotaReadExtendedPublic,
)
from tests.utils.utils import random_bool, random_lower_string, random_non_negative_int


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


def validate_public_attrs(
    *, obj_in: BlockStorageQuotaBase, db_item: BlockStorageQuota
) -> None:
    assert db_item.description == obj_in.description
    assert db_item.type == obj_in.type
    assert db_item.per_user == obj_in.per_user
    assert db_item.gigabytes == obj_in.gigabytes
    assert db_item.per_volume_gigabytes == obj_in.per_volume_gigabytes
    assert db_item.volumes == obj_in.volumes


def validate_attrs(
    *, obj_in: BlockStorageQuotaBase, db_item: BlockStorageQuota
) -> None:
    validate_public_attrs(obj_in=obj_in, db_item=db_item)


def validate_rels(
    *,
    obj_out: Union[BlockStorageQuotaReadExtended, BlockStorageQuotaReadExtendedPublic],
    db_item: BlockStorageQuota
) -> None:
    db_project = db_item.project.single()
    assert db_project
    assert db_project.uid == obj_out.project.uid
    db_service = db_item.service.single()
    assert db_service
    assert db_service.uid == obj_out.service.uid


def validate_create_block_storage_quota_attrs(
    *, obj_in: BlockStorageQuotaCreateExtended, db_item: BlockStorageQuota
) -> None:
    validate_attrs(obj_in=obj_in, db_item=db_item)
    db_project = db_item.project.single()
    assert db_project
    assert db_project.uuid == obj_in.project


def validate_read_block_storage_quota_attrs(
    *, obj_out: BlockStorageQuotaRead, db_item: BlockStorageQuota
) -> None:
    assert db_item.uid == obj_out.uid
    validate_attrs(obj_in=obj_out, db_item=db_item)


def validate_read_short_block_storage_quota_attrs(
    *, obj_out: BlockStorageQuotaReadShort, db_item: BlockStorageQuota
) -> None:
    assert db_item.uid == obj_out.uid
    validate_attrs(obj_in=obj_out, db_item=db_item)


def validate_read_public_block_storage_quota_attrs(
    *, obj_out: BlockStorageQuotaReadPublic, db_item: BlockStorageQuota
) -> None:
    assert db_item.uid == obj_out.uid
    validate_public_attrs(obj_in=obj_out, db_item=db_item)


def validate_read_extended_block_storage_quota_attrs(
    *, obj_out: BlockStorageQuotaReadExtended, db_item: BlockStorageQuota
) -> None:
    assert db_item.uid == obj_out.uid
    validate_attrs(obj_in=obj_out, db_item=db_item)
    validate_rels(obj_out=obj_out, db_item=db_item)


def validate_read_extended_public_block_storage_quota_attrs(
    *, obj_out: BlockStorageQuotaReadExtendedPublic, db_item: BlockStorageQuota
) -> None:
    assert db_item.uid == obj_out.uid
    validate_public_attrs(obj_in=obj_out, db_item=db_item)
    validate_rels(obj_out=obj_out, db_item=db_item)
