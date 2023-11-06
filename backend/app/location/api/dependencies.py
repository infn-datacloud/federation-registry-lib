from typing import Union

from app.location.crud import location
from app.location.models import Location
from app.location.schemas import LocationCreate, LocationUpdate
from fastapi import Depends, HTTPException, status


def valid_location_id(location_uid: str) -> Location:
    """Check given uid corresponds to an entity in the DB.

    Args:
        location_uid (UUID4): uid of the target DB entity.

    Returns:
        Location: DB entity with given uid.

    Raises:
        NotFoundError: DB entity with given uid not found.
    """

    item = location.get(uid=location_uid.replace("-", ""))
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Location '{location_uid}' not found",
        )
    return item


def valid_location_site(item: Union[LocationCreate, LocationUpdate]) -> None:
    """Check there are no other locations with the same site.

    Args:
        item (LocationCreate | LocationUpdate): input data.

    Returns:
        None

    Raises:
        BadRequestError: DB entity with given site already exists.
    """

    db_item = location.get(site=item.site)
    if db_item is not None:
        msg = f"Location with site '{item.site}' already registered"
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=msg,
        )


def validate_new_location_values(
    update_data: LocationUpdate, item: Location = Depends(valid_location_id)
) -> None:
    """Check given data are valid ones. Check there are no other locations with the same
    site.

    Args:
        update_data (FlavorUpdate): new data.
        item (Flavor): DB entity to update.

    Returns:
        None

    Raises:
        NotFoundError: DB entity with given uid not found.
        BadRequestError: DB entity with given site already exists.
    """

    if update_data.site != item.site:
        valid_location_site(update_data)
