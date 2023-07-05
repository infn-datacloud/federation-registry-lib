from fastapi import HTTPException, status
from pydantic import UUID4

from ..crud import identity_provider
from ..models import IdentityProvider


def valid_identity_provider_id(
    identity_provider_uid: UUID4,
) -> IdentityProvider:
    item = identity_provider.get(
        uid=str(identity_provider_uid).replace("-", "")
    )
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Identity Provider {identity_provider_uid} not found",
        )
    return item
