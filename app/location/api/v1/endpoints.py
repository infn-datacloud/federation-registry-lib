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
from app.location.api.dependencies import (
    valid_location_id,
    validate_new_location_values,
)
from app.location.crud import location
from app.location.models import Location
from app.location.schemas import (
    LocationQuery,
    LocationRead,
    LocationReadPublic,
    LocationUpdate,
)
from app.location.schemas_extended import (
    LocationReadExtended,
    LocationReadExtendedPublic,
)
from app.query import DbQueryCommonParams, Pagination, SchemaSize

# from app.region.models import Region
# from app.region.api.dependencies import valid_region_id

router = APIRouter(prefix="/locations", tags=["locations"])


@db.read_transaction
@router.get(
    "/",
    response_model=Union[
        List[LocationReadExtended],
        List[LocationRead],
        List[LocationReadExtendedPublic],
        List[LocationReadPublic],
    ],
    summary="Read all locations",
    description="Retrieve all locations stored in the database. \
        It is possible to filter on locations attributes and other \
        common query parameters.",
)
@flaat.inject_user_infos(strict=False)
def get_locations(
    comm: DbQueryCommonParams = Depends(),
    page: Pagination = Depends(),
    size: SchemaSize = Depends(),
    item: LocationQuery = Depends(),
    user_infos: Optional[Any] = None,
):
    items = location.get_multi(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    items = location.paginate(items=items, page=page.page, size=page.size)
    return location.choose_out_schema(
        items=items, auth=user_infos, short=size.short, with_conn=size.with_conn
    )


@db.read_transaction
@router.get(
    "/{location_uid}",
    response_model=Union[
        LocationReadExtended,
        LocationRead,
        LocationReadExtendedPublic,
        LocationReadPublic,
    ],
    summary="Read a specific location",
    description="Retrieve a specific location using its *uid*. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error.",
)
@flaat.inject_user_infos(strict=False)
def get_location(
    size: SchemaSize = Depends(),
    item: Location = Depends(valid_location_id),
    user_infos: Optional[Any] = None,
):
    return location.choose_out_schema(
        items=[item], auth=user_infos, short=size.short, with_conn=size.with_conn
    )[0]


@db.write_transaction
@router.patch(
    "/{location_uid}",
    status_code=status.HTTP_200_OK,
    response_model=Optional[LocationRead],
    dependencies=[
        Depends(validate_new_location_values),
    ],
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
@flaat.access_level("write")
def put_location(
    request: Request,
    update_data: LocationUpdate,
    response: Response,
    item: Location = Depends(valid_location_id),
):
    db_item = location.update(db_obj=item, obj_in=update_data)
    if not db_item:
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
        raises a `not found` error. \
        If the deletion procedure fails, raises a `internal \
        server` error",
)
@flaat.access_level("write")
def delete_location(
    request: Request,
    item: Location = Depends(valid_location_id),
    client_credentials: HTTPBasicCredentials = Security(security),
):
    if not location.remove(db_obj=item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )


# @db.write_transaction
# @router.put(
#     "/{location_uid}/regions/{region_uid}",
#     response_model=Optional[LocationReadExtended],
#
#     summary="Connect location to region",
#     description="Connect a location to a specific region \
#         knowing their *uid*s. \
#         If the location already has a \
#         current region and the new one is different, \
#         the endpoint replaces it with the new one, otherwise \
#         it leaves the entity unchanged and returns a \
#         `not modified` message. \
#         If no entity matches the given *uid*s, the endpoint \
#         raises a `not found` error.",
# )
# def connect_location_to_region(
#     response: Response,
#     item: Location = Depends(valid_location_id),
#     r_egion: Region = Depends(valid_region_id),
# ):
#     if not item.region.single():
#         item.region.connect(region)
#     elif not item.region.is_connected(region):
#         item.region.replace(region)
#     else:
#         response.status_code = status.HTTP_304_NOT_MODIFIED
#         return None
#     return item


# @db.write_transaction
# @router.delete(
#     "/{location_uid}/regions/{region_uid}",
#     response_model=Optional[LocationReadExtended],
#
#     summary="Disconnect location from region",
#     description="Disconnect a location from a specific region \
#         knowing their *uid*s. \
#         If no entity matches the given *uid*s, the endpoint \
#         raises a `not found` error.",
# )
# def disconnect_location_from_region(
#     response: Response,
#     item: Location = Depends(valid_location_id),
#     r_egion: Region = Depends(valid_region_id),
# ):
#     if not item.region.is_connected(region):
#         response.status_code = status.HTTP_304_NOT_MODIFIED
#         return None
#     item.region.disconnect(region)
#     return item
