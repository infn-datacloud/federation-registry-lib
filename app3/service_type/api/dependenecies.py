from fastapi import HTTPException, status
from pydantic import UUID4

from ..schemas import ServiceTypeCreate
from ..models import ServiceType
from ..crud import read_service_type


def valid_service_type_id(service_type_uid: UUID4) -> ServiceType:
    item = read_service_type(uid=str(service_type_uid).replace("-", ""))
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Service Type {service_type_uid} not found",
        )
    return item


def is_unique_service_type(item: ServiceTypeCreate) -> ServiceTypeCreate:
    print(item)
    db_item = read_service_type(name=item.name)
    if db_item is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Service Type with name '{item.name}' already registered",
        )
    return item
