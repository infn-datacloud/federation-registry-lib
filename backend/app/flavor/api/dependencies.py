from fastapi import Depends, HTTPException, status
from pydantic import UUID4

from app.flavor.crud import flavor
from app.flavor.models import Flavor
from app.flavor.schemas import FlavorUpdate
from app.utils import find_duplicates


def valid_flavor_id(flavor_uid: UUID4) -> Flavor:
    """
    Check given uid corresponds to an entity in the DB.

    Args:
        flavor_uid (UUID4): uid of the target DB entity.

    Returns:
        Flavor: DB entity with given uid.

    Raises:
        NotFoundError: DB entity with given uid not found.
    """

    item = flavor.get(uid=str(flavor_uid).replace("-", ""))
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Flavor '{flavor_uid}' not found",
        )
    return item


def validate_new_flavor_values(
    update_data: FlavorUpdate, item: Flavor = Depends(valid_flavor_id)
) -> None:
    """
    Check given data are valid ones. Check there are no other flavors,
    belonging to the same provider, with the same uuid and name.

    Args:
        update_data (FlavorUpdate): new data.
        item (Flavor): DB entity to update.

    Returns:
        None

    Raises:
        NotFoundError: DB entity with given uid not found.
        BadRequestError: DB entity with identical name or uuid, 
            belonging to the same provider, already exists.
    """
    
    if update_data.name != item.name:
        find_duplicates(item.provider.single().flavors.all(), "name")
    if str(update_data.uuid) != item.uuid:
        find_duplicates(item.provider.single().flavors.all(), "uuid")
