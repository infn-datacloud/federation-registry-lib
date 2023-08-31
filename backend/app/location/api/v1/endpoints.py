from typing import List, Optional

from app.auth.dependencies import flaat
from app.location.api.dependencies import (
    valid_location_id,
    valid_location_name,
    validate_new_location_values,
)
from app.location.crud import location
from app.location.models import Location
from app.location.schemas import LocationCreate, LocationQuery, LocationUpdate
from app.location.schemas_extended import LocationReadExtended
from app.pagination import Pagination, paginate
from app.query import CommonGetQuery
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from neomodel import db

router = APIRouter(prefix="/locations", tags=["locations"])


@db.read_transaction
@router.get(
    "/",
    response_model=List[LocationReadExtended],
    summary="Read all locations",
    description="Retrieve all locations stored in the database. \
        It is possible to filter on locations attributes and other \
        common query parameters.",
)
@flaat.is_authenticated()
def get_locations(
    request: Request,
    comm: CommonGetQuery = Depends(),
    page: Pagination = Depends(),
    item: LocationQuery = Depends(),
):
    items = location.get_multi(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    return paginate(items=items, page=page.page, size=page.size)


@db.write_transaction
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=LocationReadExtended,
    dependencies=[Depends(valid_location_name)],
    summary="Create location",
    description="Create a location. \
        At first validate new location values checking there are \
        no other items with the given *name*.",
)
@flaat.access_level("write")
def post_location(request: Request, item: LocationCreate):
    return location.create(obj_in=item, force=True)


@db.read_transaction
@router.get(
    "/{location_uid}",
    response_model=LocationReadExtended,
    summary="Read a specific location",
    description="Retrieve a specific location using its *uid*. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error.",
)
@flaat.is_authenticated()
def get_location(request: Request, item: Location = Depends(valid_location_id)):
    return item


@db.write_transaction
@router.patch(
    "/{location_uid}",
    response_model=Optional[LocationReadExtended],
    dependencies=[Depends(validate_new_location_values)],
    summary="Edit a specific Location",
    description="Update attribute values of a specific location. \
        The target location is identified using its uid. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error. If new values equal \
        current ones, the database entity is left unchanged \
        and the endpoint returns the `not modified` message. \
        At first validate new location values checking there are \
        no other items with the given *name*.",
)
@flaat.access_level("write")
def put_location(
    request: Request,
    update_data: LocationUpdate,
    response: Response,
    item: Location = Depends(valid_location_id),
):
    db_item = location.update(db_obj=item, obj_in=update_data)
    if db_item is None:
        response.status_code = status.HTTP_304_NOT_MODIFIED
    return db_item


@db.write_transaction
@router.delete(
    "/{location_uid}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a specific location",
    description="Delete a specific location using its *uid*. \
        Returns `no content`. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error.",
)
@flaat.access_level("write")
def delete_location(request: Request, item: Location = Depends(valid_location_id)):
    if not location.remove(db_obj=item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )
