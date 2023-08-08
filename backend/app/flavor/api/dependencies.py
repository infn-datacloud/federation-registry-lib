from fastapi import Depends, HTTPException, status
from pydantic import UUID4
from typing import Union

from app.flavor.crud import flavor
from app.flavor.models import Flavor
from app.flavor.schemas import FlavorCreate, FlavorUpdate
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


def valid_flavor_name(
    item: Union[FlavorCreate, FlavorUpdate],
    provider: Provider = Depends(valid_provider_id),
) -> None:
    """
    Check there are no other flavors, belonging to the same
    provider, with the same name.

    Args:
        item (FlavorCreate | FlavorUpdate): new data.

    Returns:
        None

    Raises:
        BadRequestError: DB entity with identical name,
            belonging to the same provider, already exists.
    """

    db_item = provider.flavors.get_or_none(name=item.name)
    if db_item is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Flavor with name '{item.name}' already registered",
        )


def valid_flavor_uuid(
    item: Union[FlavorCreate, FlavorUpdate],
    provider: Provider = Depends(valid_provider_id),
) -> None:
    """
    Check there are no other flavors, belonging to the same
    provider, with the same uuid.

    Args:
        item (FlavorCreate | FlavorUpdate): new data.

    Returns:
        None

    Raises:
        BadRequestError: DB entity with identical uuid,
            belonging to the same provider, already exists.
    """
    db_item = provider.flavors.get_or_none(uuid=item.uuid)
    if db_item is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Flavor with uuid '{item.uuid}' already registered",
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
        valid_flavor_name(item=update_data, provider=item.provider.single())
    if str(update_data.uuid) != item.uuid:
        valid_flavor_uuid(item=update_data, provider=item.provider.single())
