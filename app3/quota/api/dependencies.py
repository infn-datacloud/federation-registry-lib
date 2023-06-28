from fastapi import HTTPException, status
from pydantic import UUID4

from ..crud import quota
from ..models import Quota


def valid_quota_id(quota_uid: UUID4) -> Quota:
    item = quota.get(uid=str(quota_uid).replace("-", ""))
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Quota {quota_uid} not found",
        )
    return item
