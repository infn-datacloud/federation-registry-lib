from fastapi import Depends, HTTPException, status
from pydantic import UUID4

from app.image.crud import image
from app.image.models import Image
from app.image.schemas import ImageUpdate
from app.provider.api.dependencies import valid_provider_id
from app.provider.models import Provider


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

def is_unique_image(
    *,
    item: ImageUpdate,
    attr: str,
    provider: Provider = Depends(valid_provider_id),
) -> None:
    """
    Check there are no other images, belonging to the same
    provider, with the same name or uuid.

    Args:
        item (ImageUpdate): new data.

    Returns:
        None

    Raises:
        BadRequestError: DB entity with identical name or uuid,
            belonging to the same provider, already exists.
    """

    kwargs = {attr: item.__getattribute__(attr)}
    db_item = provider.images.get_or_none(**kwargs)
    if db_item is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Image with {attr} '{kwargs[attr]}' already registered",
        )


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
        is_unique_image(
            item=update_data, provider=item.provider.single(), attr="name"
        )
    if str(update_data.uuid) != item.uuid:
        is_unique_image(
            item=update_data, provider=item.provider.single(), attr="uuid"
        )
