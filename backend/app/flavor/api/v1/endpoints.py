from fastapi import APIRouter, Depends, HTTPException, Response, status
from neomodel import db
from typing import List, Optional

from app.flavor.api.dependencies import (
    valid_flavor_id,
    validate_new_flavor_values,
)
from app.flavor.crud import flavor
from app.flavor.models import Flavor
from app.flavor.schemas import FlavorQuery, FlavorUpdate
from app.flavor.schemas_extended import FlavorReadExtended
from app.pagination import Pagination, paginate
from app.query import CommonGetQuery

router = APIRouter(prefix="/flavors", tags=["flavors"])


@db.read_transaction
@router.get(
    "/",
    response_model=List[FlavorReadExtended],
    summary="Read all flavors",
    description="Retrieve all flavors stored in the database. \
        It is possible to filter on flavors attributes and other \
        common query parameters.",
)
def get_flavors(
    comm: CommonGetQuery = Depends(),
    page: Pagination = Depends(),
    item: FlavorQuery = Depends(),
):
    items = flavor.get_multi(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    return paginate(items=items, page=page.page, size=page.size)


@db.read_transaction
@router.get(
    "/{flavor_uid}",
    response_model=FlavorReadExtended,
    summary="Read a specific flavor",
    description="Retrieve a specific flavor using its *uid*. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error.",
)
def get_flavor(item: Flavor = Depends(valid_flavor_id)):
    return item


@db.write_transaction
@router.put(
    "/{flavor_uid}",
    response_model=Optional[FlavorReadExtended],
    dependencies=[Depends(validate_new_flavor_values)],
    summary="Edit a specific flavor",
    description="Update attribute values of a specific flavor. \
        The target flavor is identified using its *uid*. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error. If new values equal \
        current ones, the database entity is left unchanged \
        and the endpoint returns the `not modified` message. \
        At first validate new flavor values checking there are \
        no other items with the given *uuid* and *name*.",
)
def put_flavor(
    update_data: FlavorUpdate,
    response: Response,
    item: Flavor = Depends(valid_flavor_id),
):
    db_item = flavor.update(db_obj=item, obj_in=update_data)
    if db_item is None:
        response.status_code = status.HTTP_304_NOT_MODIFIED
    return db_item


@db.write_transaction
@router.delete(
    "/{flavor_uid}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a specific flavor",
    description="Delete a specific flavor using its *uid*. \
        Returns `no content`. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error.",
)
def delete_flavors(item: Flavor = Depends(valid_flavor_id)):
    if not flavor.remove(db_obj=item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )
