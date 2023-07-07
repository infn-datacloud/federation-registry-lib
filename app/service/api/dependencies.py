from fastapi import HTTPException, status
from pydantic import UUID4

from ..crud import service
from ..models import Service
from ..schemas import ServiceCreate


def valid_service_id(service_uid: UUID4) -> Service:
    item = service.get(uid=str(service_uid).replace("-", ""))
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Service {service_uid} not found",
        )
    return item


def is_unique_service(item: ServiceCreate) -> ServiceCreate:
    db_item = service.get(endpoint=item.endpoint)
    if db_item is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Service with URL '{item.endpoint}' already registered",
        )
    return item
