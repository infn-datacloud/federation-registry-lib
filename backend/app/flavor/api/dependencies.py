from fastapi import Depends, HTTPException, status
from pydantic import UUID4

from app.flavor.crud import flavor
from app.flavor.models import Flavor
from app.flavor.schemas import FlavorUpdate
from app.provider.api.dependencies import valid_provider_id
from app.provider.models import Provider


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


def is_unique_flavor(
    *,
    item: FlavorUpdate,
    attr: str,
    provider: Provider = Depends(valid_provider_id),
) -> None:
    """
    Check there are no other flavors, belonging to the same
    provider, with the same name or uuid.

    Args:
        item (FlavorUpdate): new data.

    Returns:
        None

    Raises:
        BadRequestError: DB entity with identical name or uuid,
            belonging to the same provider, already exists.
    """

    kwargs = {attr: item.__getattribute__(attr)}
    db_item = provider.flavors.get_or_none(**kwargs)
    if db_item is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Flavor with {attr} '{kwargs[attr]}' already registered",
        )


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
        is_unique_flavor(
            item=update_data, provider=item.provider.single(), attr="name"
        )
    if str(update_data.uuid) != item.uuid:
        is_unique_flavor(
            item=update_data, provider=item.provider.single(), attr="uuid"
        )
