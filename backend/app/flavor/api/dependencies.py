from fastapi import Depends, HTTPException, status
from pydantic import UUID4

from app.flavor.crud import flavor
from app.flavor.models import Flavor
from app.flavor.schemas import FlavorUpdate
from app.utils import find_duplicates


def valid_flavor_id(flavor_uid: UUID4) -> Flavor:
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
    if update_data.name != item.name:
        find_duplicates(item.provider.single().flavors.all(), "name")
    if str(update_data.uuid) != item.uuid:
        find_duplicates(item.provider.single().flavors.all(), "uuid")
