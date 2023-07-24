from fastapi import Depends, HTTPException, status
from pydantic import UUID4

from app.identity_provider.crud import identity_provider
from app.identity_provider.models import IdentityProvider
from app.identity_provider.schemas import IdentityProviderUpdate


def valid_identity_provider_id(
    identity_provider_uid: UUID4,
) -> IdentityProvider:
    item = identity_provider.get(
        uid=str(identity_provider_uid).replace("-", "")
    )
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Identity Provider '{identity_provider_uid}' not found",
        )
    return item


def validate_new_identity_provider_values(
    update_data: IdentityProviderUpdate,
    item: IdentityProvider = Depends(valid_identity_provider_id),
) -> None:
    if update_data.endpoint != item.endpoint:
        db_item = identity_provider.get(endpoint=update_data.endpoint)
        if db_item is not None:
            msg = f"Identity Provider with URL '{update_data.endpoint}' "
            msg += "already registered"
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=msg,
            )
