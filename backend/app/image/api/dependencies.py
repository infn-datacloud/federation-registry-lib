from fastapi import Depends, HTTPException, status
from pydantic import UUID4
from typing import Union

from app.image.crud import image
from app.image.models import Image
from app.image.schemas import ImageCreate, ImageUpdate
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


def valid_image_name(
    item: Union[ImageCreate, ImageUpdate],
    provider: Provider = Depends(valid_provider_id),
) -> None:
    """
    Check there are no other images, belonging to the same
    provider, with the same name.

    Args:
        item (ImageCreate | ImageUpdate): new data.

    Returns:
        None

    Raises:
        BadRequestError: DB entity with identical name,
            belonging to the same provider, already exists.
    """

    db_item = provider.images.get_or_none(name=item.name)
    if db_item is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Image with name '{item.name}' already registered",
        )


def valid_image_uuid(
    item: Union[ImageCreate, ImageUpdate],
    provider: Provider = Depends(valid_provider_id),
) -> None:
    """
    Check there are no other images, belonging to the same
    provider, with the same uuid.

    Args:
        item (ImageCreate | ImageUpdate): new data.

    Returns:
        None

    Raises:
        BadRequestError: DB entity with identical uuid,
            belonging to the same provider, already exists.
    """
    db_item = provider.images.get_or_none(uuid=item.uuid)
    if db_item is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Image with uuid '{item.uuid}' already registered",
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
        valid_image_name(item=update_data, provider=item.provider.single())
    if str(update_data.uuid) != item.uuid:
        valid_image_uuid(item=update_data, provider=item.provider.single())
