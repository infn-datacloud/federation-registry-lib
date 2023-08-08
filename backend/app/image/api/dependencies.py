from fastapi import Depends, HTTPException, status
from pydantic import UUID4

from app.image.crud import image
from app.image.models import Image
from app.image.schemas import ImageUpdate
from app.utils import find_duplicates


def valid_image_id(image_uid: UUID4) -> Image:
    """
    Check given uid corresponds to an entity in the DB.

    Args:
        image_uid (UUID4): uid of the target DB entity.

    Returns:
        Image: DB entity with given uid.

    Raises:
        NotFoundError: DB entity with given uid not found.
    """

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
    """
    Check given data are valid ones. Check there are no other images,
    belonging to the same provider, with the same uuid and name.

    Args:
        update_data (ImageUpdate): new data.
        item (Image): DB entity to update.

    Returns:
        None

    Raises:
        NotFoundError: DB entity with given uid not found.
        BadRequestError: DB entity with identical name or uuid, 
            belonging to the same provider, already exists.
    """

    if update_data.name != item.name:
        find_duplicates(item.provider.single().images.all(), "name")
    if str(update_data.uuid) != item.uuid:
        find_duplicates(item.provider.single().images.all(), "uuid")
