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
from app.network.api.dependencies import (
    valid_network_id,
    validate_new_network_values,
)
from app.network.crud import network_mng
from app.network.models import Network
from app.network.schemas import (
    NetworkQuery,
    NetworkRead,
    NetworkReadPublic,
    NetworkUpdate,
)
from app.network.schemas_extended import (
    NetworkReadExtended,
    NetworkReadExtendedPublic,
)
from app.query import DbQueryCommonParams, Pagination, SchemaSize

router = APIRouter(prefix="/networks", tags=["networks"])


@db.read_transaction
@router.get(
    "/",
    response_model=Union[
        List[NetworkReadExtended],
        List[NetworkRead],
        List[NetworkReadExtendedPublic],
        List[NetworkReadPublic],
    ],
    summary="Read all networks",
    description="Retrieve all networks stored in the database. \
        It is possible to filter on networks attributes and other \
        common query parameters.",
)
@flaat.inject_user_infos(strict=False)
def get_networks(
    comm: DbQueryCommonParams = Depends(),
    page: Pagination = Depends(),
    size: SchemaSize = Depends(),
    item: NetworkQuery = Depends(),
    user_infos: Optional[Any] = None,
):
    items = network_mng.get_multi(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    items = network_mng.paginate(items=items, page=page.page, size=page.size)
    return network_mng.choose_out_schema(
        items=items, auth=user_infos, short=size.short, with_conn=size.with_conn
    )


@db.read_transaction
@router.get(
    "/{network_uid}",
    response_model=Union[
        NetworkReadExtended,
        NetworkRead,
        NetworkReadExtendedPublic,
        NetworkReadPublic,
    ],
    summary="Read a specific network",
    description="Retrieve a specific network using its *uid*. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error.",
)
@flaat.inject_user_infos(strict=False)
def get_network(
    size: SchemaSize = Depends(),
    item: Network = Depends(valid_network_id),
    user_infos: Optional[Any] = None,
):
    return network_mng.choose_out_schema(
        items=[item], auth=user_infos, short=size.short, with_conn=size.with_conn
    )[0]


@db.write_transaction
@router.patch(
    "/{network_uid}",
    status_code=status.HTTP_200_OK,
    response_model=Optional[NetworkRead],
    dependencies=[
        Depends(validate_new_network_values),
    ],
    summary="Edit a specific network",
    description="Update attribute values of a specific network. \
        The target network is identified using its uid. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error. If new values equal \
        current ones, the database entity is left unchanged \
        and the endpoint returns the `not modified` message. \
        At first validate new network values checking there are \
        no other items with the given *uuid* and *name*.",
)
@flaat.access_level("write")
def put_network(
    request: Request,
    update_data: NetworkUpdate,
    response: Response,
    item: Network = Depends(valid_network_id),
    client_credentials: HTTPBasicCredentials = Security(security),
):
    db_item = network_mng.update(db_obj=item, obj_in=update_data)
    if not db_item:
        response.status_code = status.HTTP_304_NOT_MODIFIED
    return db_item


@db.write_transaction
@router.delete(
    "/{network_uid}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a specific network",
    description="Delete a specific network using its *uid*. \
        Returns `no content`. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error. \
        If the deletion procedure fails, raises a `internal \
        server` error",
)
@flaat.access_level("write")
def delete_networks(
    request: Request,
    item: Network = Depends(valid_network_id),
    client_credentials: HTTPBasicCredentials = Security(security),
):
    if not network_mng.remove(db_obj=item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )
