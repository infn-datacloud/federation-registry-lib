from fastapi import HTTPException, status
from pydantic import UUID4

from ..crud import read_service
from ..models import Service


def valid_service_id(service_uid: UUID4) -> Service:
    item = read_service(uid=str(service_uid).replace("-", ""))
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Service {service_uid} not found",
        )
    return item