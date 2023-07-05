from fastapi import HTTPException, status
from pydantic import UUID4

from ..crud import sla
from ..models import SLA


def valid_sla_id(sla_uid: UUID4) -> SLA:
    item = sla.get(uid=str(sla_uid).replace("-", ""))
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User Group {sla_uid} not found",
        )
    return item
