from typing import List, Optional, Union

from app.auth.dependencies import check_read_access, check_write_access
from app.flavor.api.dependencies import valid_flavor_id, validate_new_flavor_values
from app.flavor.crud import flavor
from app.flavor.models import Flavor
from app.flavor.schemas import (
    FlavorQuery,
    FlavorRead,
    FlavorReadPublic,
    FlavorReadShort,
    FlavorUpdate,
)
from app.flavor.schemas_extended import FlavorReadExtended, FlavorReadExtendedPublic
from app.project.crud import project
from app.project.schemas import ProjectRead, ProjectReadPublic, ProjectReadShort
from app.project.schemas_extended import ProjectReadExtended, ProjectReadExtendedPublic
from app.query import DbQueryCommonParams, Pagination, SchemaSize
from fastapi import APIRouter, Depends, HTTPException, Response, status
from neomodel import db

router = APIRouter(prefix="/flavors", tags=["flavors"])


@db.read_transaction
@router.get(
    "/",
    response_model=Union[
        List[FlavorReadExtended],
        List[FlavorRead],
        List[FlavorReadShort],
        List[FlavorReadExtendedPublic],
        List[FlavorReadPublic],
    ],
    summary="Read all flavors",
    description="Retrieve all flavors stored in the database. \
        It is possible to filter on flavors attributes and other \
        common query parameters.",
)
def get_flavors(
    auth: bool = Depends(check_read_access),
    comm: DbQueryCommonParams = Depends(),
    page: Pagination = Depends(),
    size: SchemaSize = Depends(),
    item: FlavorQuery = Depends(),
):
    items = flavor.get_multi(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    items = flavor.paginate(items=items, page=page.page, size=page.size)
    return flavor.choose_out_schema(
        items=items, auth=auth, short=size.short, with_conn=size.with_conn
    )


@db.read_transaction
@router.get(
    "/{flavor_uid}",
    response_model=Union[
        FlavorReadExtended,
        FlavorRead,
        FlavorReadShort,
        FlavorReadExtendedPublic,
        FlavorReadPublic,
    ],
    summary="Read a specific flavor",
    description="Retrieve a specific flavor using its *uid*. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error.",
)
def get_flavor(
    auth: bool = Depends(check_read_access),
    size: SchemaSize = Depends(),
    item: Flavor = Depends(valid_flavor_id),
):
    return flavor.choose_out_schema(
        items=[item], auth=auth, short=size.short, with_conn=size.with_conn
    )[0]


@db.write_transaction
@router.patch(
    "/{flavor_uid}",
    status_code=status.HTTP_200_OK,
    response_model=Optional[FlavorRead],
    dependencies=[Depends(check_write_access), Depends(validate_new_flavor_values)],
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
    dependencies=[Depends(check_write_access)],
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


@db.read_transaction
@router.get(
    "/{flavor_uid}/projects",
    response_model=Union[
        List[ProjectReadExtended],
        List[ProjectRead],
        List[ProjectReadShort],
        List[ProjectReadExtendedPublic],
        List[ProjectReadPublic],
    ],
    summary="Read user group accessible projects",
    description="Retrieve all the projects the user group \
        has access to thanks to its SLA. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error.",
)
def get_flavor_projects(
    auth: bool = Depends(check_read_access),
    size: SchemaSize = Depends(),
    item: Flavor = Depends(valid_flavor_id),
):
    if item.is_public:
        items = item.provider.single().projects.all()
    items = item.projects.all()
    return project.choose_out_schema(
        items=items, auth=auth, short=size.short, with_conn=size.with_conn
    )
