from fastapi import APIRouter, Depends, HTTPException, status
from neomodel import db
from typing import List, Mapping, Optional

from .utils import CommonGetQuery, Pagination, paginate
from .utils.validation import valid_image_id
from .. import crud, schemas

router = APIRouter(prefix="/images", tags=["images"])


@db.read_transaction
@router.get("/", response_model=List[schemas.Image])
def read_images(
    comm: CommonGetQuery = Depends(),
    page: Pagination = Depends(),
    item: schemas.ImageBase = Depends(),
):
    items = crud.get_images(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    return paginate(items=items, page=page.page, size=page.size)


@db.read_transaction
@router.get("/{uid}", response_model=schemas.Image)
def read_image(item: Mapping = Depends(valid_image_id)):
    return item


@db.write_transaction
@router.patch("/{uid}", response_model=Optional[schemas.Image])
def update_image(
    update_data: schemas.ImageUpdate, item: Mapping = Depends(valid_image_id)
):
    return crud.update_image(old_item=item, new_item=update_data)


@db.write_transaction
@router.delete("/{uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_images(item: Mapping = Depends(valid_image_id)):
    if not crud.remove_image(item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )
