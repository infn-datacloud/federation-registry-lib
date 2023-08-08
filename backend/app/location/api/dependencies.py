from typing import Union
from fastapi import Depends, HTTPException, status
from pydantic import UUID4

from app.location.crud import location
from app.location.models import Location
from app.location.schemas import LocationCreate, LocationUpdate


def valid_location_id(location_uid: UUID4) -> Location:
    """
    Check given uid corresponds to an entity in the DB.

    Args:
        location_uid (UUID4): uid of the target DB entity.

    Returns:
        Location: DB entity with given uid.

    Raises:
        NotFoundError: DB entity with given uid not found.
    """

    item = location.get(uid=str(location_uid).replace("-", ""))
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Location '{location_uid}' not found",
        )
    return item


def valid_location_name(item: Union[LocationCreate, LocationUpdate]) -> None:
    """
    Check there are no other locations with the same name.

    Args:
        item (LocationCreate | LocationUpdate): input data.

    Returns:
        None

    Raises:
        BadRequestError: DB entity with given name already exists.
    """

    db_item = location.get(name=item.name)
    if db_item is not None:
        msg = f"Location with name '{item.name}' already registered"
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=msg,
        )


def validate_new_location_values(
    update_data: LocationUpdate, item: Location = Depends(valid_location_id)
) -> None:
    """
    Check given data are valid ones. Check there are no other
    locations with the same name.

    Args:
        update_data (FlavorUpdate): new data.
        item (Flavor): DB entity to update.

    Returns:
        None

    Raises:
        NotFoundError: DB entity with given uid not found.
        BadRequestError: DB entity with given name already exists.
    """

    if update_data.name != item.name:
        valid_location_name(update_data)
