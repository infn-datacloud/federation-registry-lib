from typing import List, Optional

from app.auth.dependencies import check_read_access, check_write_access
from app.image.api.dependencies import valid_image_id, validate_new_image_values
from app.image.crud import image
from app.image.models import Image
from app.image.schemas import ImageQuery, ImageUpdate
from app.image.schemas_extended import ImageReadExtended
from app.query import DbQueryCommonParams, Pagination, SchemaSize
from fastapi import APIRouter, Depends, HTTPException, Response, status
from neomodel import db

router = APIRouter(prefix="/images", tags=["images"])


@db.read_transaction
@router.get(
    "/",
    response_model=List[ImageReadExtended],
    summary="Read all images",
    description="Retrieve all images stored in the database. \
        It is possible to filter on images attributes and other \
        common query parameters.",
)
def get_images(
    auth: bool = Depends(check_read_access),
    comm: DbQueryCommonParams = Depends(),
    page: Pagination = Depends(),
    size: SchemaSize = Depends(),
    item: ImageQuery = Depends(),
):
    items = image.get_multi(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    items = image.paginate(items=items, page=page.page, size=page.size)
    return image.choose_out_schema(
        items=items, auth=auth, short=size.short, with_conn=size.with_conn
    )


@db.read_transaction
@router.get(
    "/{image_uid}",
    response_model=ImageReadExtended,
    summary="Read a specific image",
    description="Retrieve a specific image using its *uid*. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error.",
)
def get_image(
    auth: bool = Depends(check_read_access),
    size: SchemaSize = Depends(),
    item: Image = Depends(valid_image_id),
):
    return image.choose_out_schema(
        items=[item], auth=auth, short=size.short, with_conn=size.with_conn
    )[0]


@db.write_transaction
@router.patch(
    "/{image_uid}",
    response_model=Optional[ImageReadExtended],
    dependencies=[Depends(check_write_access), Depends(validate_new_image_values)],
    summary="Edit a specific image",
    description="Update attribute values of a specific image. \
        The target image is identified using its uid. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error. If new values equal \
        current ones, the database entity is left unchanged \
        and the endpoint returns the `not modified` message. \
        At first validate new image values checking there are \
        no other items with the given *uuid* and *name*.",
)
def put_image(
    update_data: ImageUpdate,
    response: Response,
    item: Image = Depends(valid_image_id),
):
    db_item = image.update(db_obj=item, obj_in=update_data)
    if db_item is None:
        response.status_code = status.HTTP_304_NOT_MODIFIED
    return db_item


@db.write_transaction
@router.delete(
    "/{image_uid}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(check_write_access)],
    summary="Delete a specific image",
    description="Delete a specific image using its *uid*. \
        Returns `no content`. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error.",
)
def delete_images(item: Image = Depends(valid_image_id)):
    if not image.remove(db_obj=item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )
