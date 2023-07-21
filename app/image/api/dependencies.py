from fastapi import Depends, HTTPException, status
from pydantic import UUID4

from app.image.crud import image
from app.image.models import Image
from app.image.schemas import ImageUpdate
from app.utils import find_duplicates


def valid_image_id(image_uid: UUID4) -> Image:
    item = image.get(uid=str(image_uid).replace("-", ""))
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Image '{image_uid}' not found",
        )
    return item


def validate_new_image_values(
    update_data: ImageUpdate, item: Image = Depends(valid_image_id)
) -> None:
    if update_data.name != item.name:
        find_duplicates(item.provider.single().images.all(), "name")
    if update_data.uuid != item.uuid:
        find_duplicates(item.provider.single().images.all(), "uuid")
