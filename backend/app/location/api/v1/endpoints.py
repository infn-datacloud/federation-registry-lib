from typing import List, Optional, Union

from app.auth.dependencies import check_read_access, check_write_access
from app.location.api.dependencies import (
    valid_location_id,
    valid_location_site,
    validate_new_location_values,
)
from app.location.crud import location
from app.location.models import Location
from app.location.schemas import (
    LocationCreate,
    LocationQuery,
    LocationRead,
    LocationReadPublic,
    LocationReadShort,
    LocationUpdate,
)
from app.location.schemas_extended import (
    LocationReadExtended,
    LocationReadExtendedPublic,
)
from app.query import DbQueryCommonParams, Pagination, SchemaSize
from fastapi import APIRouter, Depends, HTTPException, Response, status
from neomodel import db

router = APIRouter(prefix="/locations", tags=["locations"])


@db.read_transaction
@router.get(
    "/",
    response_model=Union[
        List[LocationReadExtended],
        List[LocationRead],
        List[LocationReadShort],
        List[LocationReadExtendedPublic],
        List[LocationReadPublic],
    ],
    summary="Read all locations",
    description="Retrieve all locations stored in the database. \
        It is possible to filter on locations attributes and other \
        common query parameters.",
)
def get_locations(
    auth: bool = Depends(check_read_access),
    comm: DbQueryCommonParams = Depends(),
    page: Pagination = Depends(),
    size: SchemaSize = Depends(),
    item: LocationQuery = Depends(),
):
    items = location.get_multi(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    items = location.paginate(items=items, page=page.page, size=page.size)
    return location.choose_out_schema(
        items=items, auth=auth, short=size.short, with_conn=size.with_conn
    )


@db.write_transaction
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=LocationReadExtended,
    dependencies=[Depends(check_write_access), Depends(valid_location_site)],
    summary="Create location",
    description="Create a location. \
        At first validate new location values checking there are \
        no other items with the given *site*.",
)
def post_location(item: LocationCreate):
    return location.create(obj_in=item, force=True)


@db.read_transaction
@router.get(
    "/{location_uid}",
    response_model=Union[
        LocationReadExtended,
        LocationRead,
        LocationReadShort,
        LocationReadExtendedPublic,
        LocationReadPublic,
    ],
    summary="Read a specific location",
    description="Retrieve a specific location using its *uid*. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error.",
)
def get_location(
    auth: bool = Depends(check_read_access),
    size: SchemaSize = Depends(),
    item: Location = Depends(valid_location_id),
):
    return location.choose_out_schema(
        items=[item], auth=auth, short=size.short, with_conn=size.with_conn
    )[0]


@db.write_transaction
@router.patch(
    "/{location_uid}",
    status_code=status.HTTP_200_OK,
    response_model=Optional[LocationRead],
    dependencies=[Depends(check_write_access), Depends(validate_new_location_values)],
    summary="Edit a specific Location",
    description="Update attribute values of a specific location. \
        The target location is identified using its uid. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error. If new values equal \
        current ones, the database entity is left unchanged \
        and the endpoint returns the `not modified` message. \
        At first validate new location values checking there are \
        no other items with the given *site*.",
)
def put_location(
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
    dependencies=[Depends(check_write_access)],
    summary="Delete a specific location",
    description="Delete a specific location using its *uid*. \
        Returns `no content`. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error.",
)
def delete_location(item: Location = Depends(valid_location_id)):
    if not location.remove(db_obj=item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )
