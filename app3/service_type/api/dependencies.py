from fastapi import HTTPException, status
from pydantic import UUID4

from ..schemas_extended import ServiceTypeCreateExtended
from ..models import ServiceType
from ..crud import service_type


def valid_service_type_id(service_type_uid: UUID4) -> ServiceType:
    item = service_type.get(uid=str(service_type_uid).replace("-", ""))
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Service Type {service_type_uid} not found",
        )
    return item


def valid_service_type_name(service: ServiceType) -> ServiceType:
    item = service_type.get(name=service.name)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Service Type {service.name} not found",
        )
    return item


def is_unique_service_type(
    item: ServiceTypeCreateExtended,
) -> ServiceTypeCreateExtended:
    db_item = service_type.get(name=item.name)
    if db_item is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Service Type with name '{item.name}' already registered",
        )
    return item
