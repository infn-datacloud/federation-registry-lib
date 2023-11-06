from app.quota.crud import block_storage_quota, compute_quota
from app.quota.enum import QuotaType
from app.quota.models import BlockStorageQuota, ComputeQuota
from app.quota.schemas import BlockStorageQuotaUpdate, ComputeQuotaUpdate
from fastapi import Depends, HTTPException, status


def valid_block_storage_quota_id(quota_uid: str) -> BlockStorageQuota:
    """Check given uid corresponds to an entity in the DB.

    Args:
        quota_uid (UUID4): uid of the target DB entity.

    Returns:
        Service: DB entity with given uid.

    Raises:
        NotFoundError: DB entity with given uid not found.
    """

    item = block_storage_quota.get(uid=quota_uid.replace("-", ""))
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Block Storage Quota '{quota_uid}' not found",
        )
    return item


def validate_new_block_storage_quota_values(
    update_data: BlockStorageQuotaUpdate,
    item: BlockStorageQuota = Depends(valid_block_storage_quota_id),
) -> None:
    """Check given data are valid ones. Check there are no other quotas, belonging to
    the same project, with the same type and per_user flag.

    Args:
        update_data (BlockStorageQuotaUpdate): new data.
        item (BlockStorageQuota): DB entity to update.

    Returns:
        None

    Raises:
        NotFoundError: DB entity with given uid not found.
        BadRequestError: DB entity with identical name or uuid,
            belonging to the same service, already exists.
    """
    if update_data.per_user != item.per_user:
        db_project = item.project.single()
        if any(
            [
                q.per_user == update_data.per_user
                for q in db_project.quotas.all()
                if q.type == QuotaType.BLOCK_STORAGE.value
            ]
        ):
            s = "" if update_data.per_user else "not"
            msg = f"Project '{db_project.uid}' already has "
            msg += f"a Block Storage Quota to {s} apply to each user"
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)


def valid_compute_quota_id(quota_uid: str) -> ComputeQuota:
    """Check given uid corresponds to an entity in the DB.

    Args:
        quota_uid (UUID4): uid of the target DB entity.

    Returns:
        Service: DB entity with given uid.

    Raises:
        NotFoundError: DB entity with given uid not found.
    """

    item = compute_quota.get(uid=quota_uid.replace("-", ""))
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Compute Quota '{quota_uid}' not found",
        )
    return item


def validate_new_compute_quota_values(
    update_data: ComputeQuotaUpdate,
    item: ComputeQuota = Depends(valid_compute_quota_id),
) -> None:
    """Check given data are valid ones. Check there are no other quotas, belonging to
    the same project, with the same type and per_user flag.

    Args:
        update_data (ComputeQuotaUpdate): new data.
        item (ComputeQuota): DB entity to update.

    Returns:
        None

    Raises:
        NotFoundError: DB entity with given uid not found.
        BadRequestError: DB entity with identical name or uuid,
            belonging to the same service, already exists.
    """
    if update_data.per_user != item.per_user:
        db_project = item.project.single()
        if any(
            [
                q.per_user == update_data.per_user
                for q in db_project.quotas.all()
                if q.type == QuotaType.COMPUTE.value
            ]
        ):
            s = "" if update_data.per_user else "not"
            msg = f"Project '{db_project.uid}' already has "
            msg += f"a Compute Quota to {s} apply to each user"
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)
