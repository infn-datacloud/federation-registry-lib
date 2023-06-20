from fastapi import APIRouter, Depends, HTTPException, status
from neomodel import db
from typing import List, Mapping, Optional

from .utils import CommonGetQuery, Pagination, paginate
from .utils.validation import valid_image_id
from ..schemas import Image, ImagePatch, ImageQuery
from ..crud.image import edit_image, read_images, remove_image

router = APIRouter(prefix="/images", tags=["images"])


@db.read_transaction
@router.get("/", response_model=List[Image])
def get_images(
    comm: CommonGetQuery = Depends(),
    page: Pagination = Depends(),
    item: ImageQuery = Depends(),
):
    items = read_images(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    return paginate(items=items, page=page.page, size=page.size)


@db.read_transaction
@router.get("/{uid}", response_model=Image)
def get_image(item: Mapping = Depends(valid_image_id)):
    return item


@db.write_transaction
@router.patch("/{uid}", response_model=Optional[Image])
def patch_image(
    update_data: ImagePatch, item: Mapping = Depends(valid_image_id)
):
    return edit_image(old_item=item, new_item=update_data)


@db.write_transaction
@router.delete("/{uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_images(item: Mapping = Depends(valid_image_id)):
    if not remove_image(item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )
