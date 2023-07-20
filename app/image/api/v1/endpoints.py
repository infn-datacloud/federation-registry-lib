from fastapi import APIRouter, Depends, HTTPException, status
from neomodel import db
from typing import List, Optional

from app.image.api.dependencies import valid_image_id
from app.image.crud import image
from app.image.models import Image
from app.image.schemas import ImageQuery, ImageUpdate
from app.image.schemas_extended import ImageReadExtended
from app.pagination import Pagination, paginate
from app.query import CommonGetQuery

router = APIRouter(prefix="/images", tags=["images"])


@db.read_transaction
@router.get("/", response_model=List[ImageReadExtended])
def get_images(
    comm: CommonGetQuery = Depends(),
    page: Pagination = Depends(),
    item: ImageQuery = Depends(),
):
    items = image.get_multi(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    return paginate(items=items, page=page.page, size=page.size)


@db.read_transaction
@router.get("/{image_uid}", response_model=ImageReadExtended)
def get_image(item: Image = Depends(valid_image_id)):
    return item


@db.write_transaction
@router.put("/{image_uid}", response_model=Optional[ImageReadExtended])
def put_image(update_data: ImageUpdate, item: Image = Depends(valid_image_id)):
    return image.update(db_obj=item, obj_in=update_data)


@db.write_transaction
@router.delete("/{image_uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_images(item: Image = Depends(valid_image_id)):
    if not image.remove(db_obj=item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )
