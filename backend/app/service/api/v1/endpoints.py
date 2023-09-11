from typing import List, Optional, Union

from app.auth.dependencies import check_read_access, check_write_access
from app.identity_provider.crud import identity_provider
from app.identity_provider.schemas import (
    IdentityProviderRead,
    IdentityProviderReadPublic,
    IdentityProviderReadShort,
)
from app.identity_provider.schemas_extended import (
    IdentityProviderReadExtended,
    IdentityProviderReadExtendedPublic,
)
from app.query import DbQueryCommonParams, Pagination, SchemaSize
from app.service.api.dependencies import valid_service_id, validate_new_service_values
from app.service.crud import service
from app.service.models import Service
from app.service.schemas import (
    CinderServiceRead,
    CinderServiceReadPublic,
    CinderServiceReadShort,
    CinderServiceUpdate,
    KeystoneServiceRead,
    KeystoneServiceReadPublic,
    KeystoneServiceReadShort,
    KeystoneServiceUpdate,
    NovaServiceRead,
    NovaServiceReadPublic,
    NovaServiceReadShort,
    NovaServiceUpdate,
    ServiceQuery,
)
from app.service.schemas_extended import (
    CinderServiceReadExtended,
    CinderServiceReadExtendedPublic,
    KeystoneServiceReadExtended,
    KeystoneServiceReadExtendedPublic,
    NovaServiceReadExtended,
    NovaServiceReadExtendedPublic,
)
from fastapi import APIRouter, Depends, HTTPException, Response, status
from neomodel import db

router = APIRouter(prefix="/services", tags=["services"])


@db.read_transaction
@router.get(
    "/",
    response_model=Union[
        List[
            Union[
                CinderServiceReadExtended,
                KeystoneServiceReadExtended,
                NovaServiceReadExtended,
            ]
        ],
        List[Union[CinderServiceRead, KeystoneServiceRead, NovaServiceRead]],
        List[
            Union[
                CinderServiceReadShort, KeystoneServiceReadShort, NovaServiceReadShort
            ]
        ],
        List[
            Union[
                CinderServiceReadExtendedPublic,
                KeystoneServiceReadExtendedPublic,
                NovaServiceReadExtendedPublic,
            ]
        ],
        List[
            Union[
                CinderServiceReadPublic,
                KeystoneServiceReadPublic,
                NovaServiceReadPublic,
            ]
        ],
    ],
    summary="Read all services",
    description="Retrieve all services stored in the database. \
        It is possible to filter on services attributes and other \
        common query parameters.",
)
def get_services(
    auth: bool = Depends(check_read_access),
    comm: DbQueryCommonParams = Depends(),
    page: Pagination = Depends(),
    size: SchemaSize = Depends(),
    item: ServiceQuery = Depends(),
):
    items = service.get_multi(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    items = service.paginate(items=items, page=page.page, size=page.size)
    return service.choose_out_schema(
        items=items, auth=auth, short=size.short, with_conn=size.with_conn
    )


@db.read_transaction
@router.get(
    "/{service_uid}",
    response_model=Union[
        CinderServiceReadExtended,
        KeystoneServiceReadExtended,
        NovaServiceReadExtended,
        CinderServiceRead,
        KeystoneServiceRead,
        NovaServiceRead,
        CinderServiceReadShort,
        KeystoneServiceReadShort,
        NovaServiceReadShort,
        CinderServiceReadExtendedPublic,
        KeystoneServiceReadExtendedPublic,
        NovaServiceReadExtendedPublic,
        CinderServiceReadPublic,
        KeystoneServiceReadPublic,
        NovaServiceReadPublic,
    ],
    summary="Read a specific service",
    description="Retrieve a specific service using its *uid*. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error.",
)
def get_service(
    auth: bool = Depends(check_read_access),
    size: SchemaSize = Depends(),
    item: Service = Depends(valid_service_id),
):
    return service.choose_out_schema(
        items=[item], auth=auth, short=size.short, with_conn=size.with_conn
    )[0]


@db.write_transaction
@router.patch(
    "/{service_uid}",
    response_model=Optional[
        Union[CinderServiceRead, KeystoneServiceRead, NovaServiceRead]
    ],
    dependencies=[Depends(check_write_access), Depends(validate_new_service_values)],
    summary="Edit a specific service",
    description="Update attribute values of a specific service. \
        The target service is identified using its uid. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error. If new values equal \
        current ones, the database entity is left unchanged \
        and the endpoint returns the `not modified` message. \
        At first validate new service values checking there are \
        no other items with the given *endpoint*.",
)
def put_service(
    update_data: Union[CinderServiceUpdate, KeystoneServiceUpdate, NovaServiceUpdate],
    response: Response,
    item: Service = Depends(valid_service_id),
):
    db_item = service.update(db_obj=item, obj_in=update_data)
    if db_item is None:
        response.status_code = status.HTTP_304_NOT_MODIFIED
    return db_item


@db.write_transaction
@router.delete(
    "/{service_uid}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(check_write_access)],
    summary="Delete a specific service",
    description="Delete a specific service using its *uid*. \
        Returns `no content`. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error. \
        On cascade, delete related quotas.",
)
def delete_services(item: Service = Depends(valid_service_id)):
    if not service.remove(db_obj=item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )


@db.read_transaction
@router.get(
    "/{service_uid}/identity_providers",
    response_model=Union[
        List[IdentityProviderReadExtended],
        List[IdentityProviderRead],
        List[IdentityProviderReadShort],
        List[IdentityProviderReadExtendedPublic],
        List[IdentityProviderReadPublic],
    ],
    summary="Read service accessible identity providers",
    description="Retrieve all the identity providers the \
        service has access to. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error.",
)
def get_service_identity_providers(
    auth: bool = Depends(check_read_access),
    size: SchemaSize = Depends(),
    item: Service = Depends(valid_service_id),
):
    items = item.provider.single().identity_providers.all()
    return identity_provider.choose_out_schema(
        items=items, auth=auth, short=size.short, with_conn=size.with_conn
    )
