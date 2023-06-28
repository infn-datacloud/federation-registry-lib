from fastapi import HTTPException, status
from pydantic import UUID4

from ..crud import quota_type
from ..models import QuotaType


def valid_quota_type_id(quota_type_uid: UUID4) -> QuotaType:
    item = quota_type.get(uid=str(quota_type_uid).replace("-", ""))
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Quota Type {quota_type_uid} not found",
        )
    return item
