from fastapi import HTTPException, status
from pydantic import UUID4

from ..crud import location
from ..models import Location


def valid_location_id(location_uid: UUID4) -> Location:
    item = location.get(uid=str(location_uid).replace("-", ""))
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Location {location_uid} not found",
        )
    return item