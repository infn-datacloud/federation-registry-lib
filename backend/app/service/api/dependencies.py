from typing import Union

from app.service.crud import (
    block_storage_service,
    compute_service,
    identity_service,
    network_service,
)
from app.service.models import (
    BlockStorageService,
    ComputeService,
    IdentityService,
    NetworkService,
    Service,
)
from app.service.schemas import ServiceCreate, ServiceUpdate
from fastapi import Depends, HTTPException, status
from pydantic import UUID4


def valid_service_id(
    service_uid: UUID4,
) -> Union[BlockStorageService, ComputeService, IdentityService, NetworkService]:
    """Check given uid corresponds to an entity in the DB.

    Args:
        service_uid (UUID4): uid of the target DB entity.

    Returns:
        Service: DB entity with given uid.

    Raises:
        NotFoundError: DB entity with given uid not found.
    """

    item = block_storage_service.get(uid=str(service_uid).replace("-", ""))
    if not item:
        item = compute_service.get(uid=str(service_uid).replace("-", ""))
    if not item:
        item = identity_service.get(uid=str(service_uid).replace("-", ""))
    if not item:
        item = network_service.get(uid=str(service_uid).replace("-", ""))

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Service '{service_uid}' not found",
        )
    return item


def valid_service_endpoint(item: Union[ServiceCreate, ServiceUpdate]) -> None:
    """Check there are no other services with the same endpoint.

    Args:
        item (ServiceCreate | ServiceUpdate): new data.

    Returns:
        None

    Raises:
        BadRequestError: DB entity with given endpoint already exists.
    """

    db_item = block_storage_service.get(endpoint=item.endpoint)
    if not db_item:
        db_item = compute_service.get(endpoint=item.endpoint)
    if not db_item:
        db_item = identity_service.get(endpoint=item.endpoint)
    if not db_item:
        db_item = network_service.get(endpoint=item.endpoint)

    if db_item is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Service with URL '{item.endpoint}' already registered",
        )


def validate_new_service_values(
    update_data: ServiceUpdate, item: Service = Depends(valid_service_id)
) -> None:
    """Check given data are valid ones. Check there are no other services with
    the same endpoint.

    Args:
        update_data (FlavorUpdate): new data.
        item (Flavor): DB entity to update.

    Returns:
        None

    Raises:
        NotFoundError: DB entity with given uid not found.
        BadRequestError: DB entity with given endpoint already exists.
    """

    if str(update_data.endpoint) != item.endpoint:
        valid_service_endpoint(update_data)
    if update_data.type != item.type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Service type update is forbidden!",
        )
