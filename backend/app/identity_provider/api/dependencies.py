from typing import Union
from fastapi import Depends, HTTPException, status
from pydantic import UUID4

from app.identity_provider.crud import identity_provider
from app.identity_provider.models import IdentityProvider
from app.identity_provider.schemas import (
    IdentityProviderCreate,
    IdentityProviderUpdate,
)


def valid_identity_provider_id(
    identity_provider_uid: UUID4,
) -> IdentityProvider:
    """
    Check given uid corresponds to an entity in the DB.

    Args:
        identity_provider_uid (UUID4): uid of the target DB entity.

    Returns:
        IdentityProvider: DB entity with given uid.

    Raises:
        NotFoundError: DB entity with given uid not found.
    """

    item = identity_provider.get(
        uid=str(identity_provider_uid).replace("-", "")
    )
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Identity Provider '{identity_provider_uid}' not found",
        )
    return item


def valid_identity_provider_endpoint(
    item: Union[IdentityProviderCreate, IdentityProviderUpdate]
) -> None:
    """
    Check there are no other identity providers with the same endpoint.

    Args:
        item (IdentityProviderCreate | IdentityProviderUpdate): input data.

    Returns:
        None

    Raises:
        BadRequestError: DB entity with given endpoint already exists.
    """

    db_item = identity_provider.get(endpoint=item.endpoint)
    if db_item is not None:
        msg = f"Identity Provider with URL '{item.endpoint}' "
        msg += "already registered"
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=msg,
        )


def validate_new_identity_provider_values(
    update_data: IdentityProviderUpdate,
    item: IdentityProvider = Depends(valid_identity_provider_id),
) -> None:
    """
    Check given data are valid ones. Check there are no other
    identity providers with the same endpoint.

    Args:
        update_data (IdentityProviderUpdate): new data.
        item (IdentityProvider): DB entity to update.

    Returns:
        None

    Raises:
        NotFoundError: DB entity with given uid not found.
        BadRequestError: DB entity with given endpoint already exists.
    """

    if str(update_data.endpoint) != item.endpoint:
        valid_identity_provider_endpoint(update_data)
