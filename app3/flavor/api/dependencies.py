from fastapi import HTTPException, status
from pydantic import UUID4

from ..crud import flavor
from ..models import Flavor


def valid_flavor_id(flavor_uid: UUID4) -> Flavor:
    item = flavor.get(uid=str(flavor_uid).replace("-", ""))
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Flavor {flavor_uid} not found",
        )
    return item