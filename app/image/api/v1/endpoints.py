from typing import Any, List, Optional, Union

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    Response,
    Security,
    status,
)
from fastapi.security import HTTPBasicCredentials
from neomodel import db

from app.auth import flaat, security
from app.image.api.dependencies import (
    valid_image_id,
    validate_new_image_values,
)
from app.image.crud import image
from app.image.models import Image
from app.image.schemas import (
    ImageQuery,
    ImageRead,
    ImageReadPublic,
    ImageUpdate,
)
from app.image.schemas_extended import (
    ImageReadExtended,
    ImageReadExtendedPublic,
)
from app.query import DbQueryCommonParams, Pagination, SchemaSize

router = APIRouter(prefix="/images", tags=["images"])


@db.read_transaction
@router.get(
    "/",
    response_model=Union[
        List[ImageReadExtended],
        List[ImageRead],
        List[ImageReadExtendedPublic],
        List[ImageReadPublic],
    ],
    summary="Read all images",
    description="Retrieve all images stored in the database. \
        It is possible to filter on images attributes and other \
        common query parameters.",
)
@flaat.inject_user_infos(strict=False)
def get_images(
    comm: DbQueryCommonParams = Depends(),
    page: Pagination = Depends(),
    size: SchemaSize = Depends(),
    item: ImageQuery = Depends(),
    user_infos: Optional[Any] = None,
):
    items = image.get_multi(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    items = image.paginate(items=items, page=page.page, size=page.size)
    return image.choose_out_schema(
        items=items, auth=user_infos, with_conn=size.with_conn
    )


@db.read_transaction
@router.get(
    "/{image_uid}",
    response_model=Union[
        ImageReadExtended,
        ImageRead,
        ImageReadExtendedPublic,
        ImageReadPublic,
    ],
    summary="Read a specific image",
    description="Retrieve a specific image using its *uid*. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error.",
)
@flaat.inject_user_infos(strict=False)
def get_image(
    size: SchemaSize = Depends(),
    item: Image = Depends(valid_image_id),
    user_infos: Optional[Any] = None,
):
    return image.choose_out_schema(
        items=[item], auth=user_infos, with_conn=size.with_conn
    )[0]


@db.write_transaction
@router.patch(
    "/{image_uid}",
    status_code=status.HTTP_200_OK,
    response_model=Optional[ImageRead],
    dependencies=[
        Depends(validate_new_image_values),
    ],
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
@flaat.access_level("write")
def put_image(
    request: Request,
    update_data: ImageUpdate,
    response: Response,
    item: Image = Depends(valid_image_id),
    client_credentials: HTTPBasicCredentials = Security(security),
):
    db_item = image.update(db_obj=item, obj_in=update_data)
    if not db_item:
        response.status_code = status.HTTP_304_NOT_MODIFIED
    return db_item


@db.write_transaction
@router.delete(
    "/{image_uid}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a specific image",
    description="Delete a specific image using its *uid*. \
        Returns `no content`. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error. \
        If the deletion procedure fails, raises a `internal \
        server` error",
)
@flaat.access_level("write")
def delete_images(
    request: Request,
    item: Image = Depends(valid_image_id),
    client_credentials: HTTPBasicCredentials = Security(security),
):
    if not image.remove(db_obj=item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )
