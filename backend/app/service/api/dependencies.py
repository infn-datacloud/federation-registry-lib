from fastapi import Depends, HTTPException, status
from pydantic import UUID4

from app.service.crud import service
from app.service.models import Service
from app.service.schemas import ServiceCreate, ServiceUpdate


def valid_service_id(service_uid: UUID4) -> Service:
    item = service.get(uid=str(service_uid).replace("-", ""))
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Service '{service_uid}' not found",
        )
    return item


def is_unique_service(item: ServiceCreate) -> None:
    db_item = service.get(endpoint=item.endpoint)
    if db_item is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Service with URL '{item.endpoint}' already registered",
        )


def validate_new_service_values(
    update_data: ServiceUpdate, item: Service = Depends(valid_service_id)
) -> None:
    if str(update_data.endpoint) != item.endpoint:
        is_unique_service(update_data)
