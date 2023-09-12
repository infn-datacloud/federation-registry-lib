from app.quota.crud import quota
from app.quota.models import Quota
from fastapi import HTTPException, status
from pydantic import UUID4


def valid_quota_id(quota_uid: UUID4) -> Quota:
    """Check given uid corresponds to an entity in the DB.

    Args:
        quota_uid (UUID4): uid of the target DB entity.

    Returns:
        Service: DB entity with given uid.

    Raises:
        NotFoundError: DB entity with given uid not found.
    """

    item = quota.get(uid=str(quota_uid).replace("-", ""))
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Quota '{quota_uid}' not found",
        )
    return item
