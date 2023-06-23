from fastapi import HTTPException, status
from pydantic import UUID4

from .crud import read_quota
from .models import Quota
from ..service.dependencies import valid_service_id
from ..service.models import Service


def valid_quota_id(quota_uid: UUID4) -> Quota:
    item = read_quota(uid=str(quota_uid).replace("-", ""))
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Quota {quota_uid} not found",
        )
    return item


def validate_quota(quota: Quota, service: Service) -> Quota:
    srv_type = service.type.single()
    allowed_quota_types = [t.name for t in srv_type.quota_types.all()]
    if quota.type.name not in allowed_quota_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Quota '{quota.type.name}' can't be applied on services of type '{srv_type}'",
        )
    return quota
