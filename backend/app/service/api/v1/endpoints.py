from typing import List, Optional, Union

from app.auth.dependencies import flaat
from app.identity_provider.schemas import IdentityProviderRead
from app.pagination import Pagination, paginate
from app.query import CommonGetQuery
from app.service.api.dependencies import valid_service_id, validate_new_service_values
from app.service.crud import service
from app.service.models import Service
from app.service.schemas import KubernetesServiceUpdate, NovaServiceUpdate, ServiceQuery
from app.service.schemas_extended import (
    KubernetesServiceReadExtended,
    NovaServiceReadExtended,
)
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from neomodel import db

router = APIRouter(prefix="/services", tags=["services"])


@db.read_transaction
@router.get(
    "/",
    response_model=List[
        Union[
            # ChronosServiceReadExtended,
            KubernetesServiceReadExtended,
            # MarathonServiceReadExtended,
            # MesosServiceReadExtended,
            NovaServiceReadExtended,
            # OneDataServiceReadExtended,
            # RucioServiceReadExtended,
        ]
    ],
    summary="Read all services",
    description="Retrieve all services stored in the database. \
        It is possible to filter on services attributes and other \
        common query parameters.",
)
@flaat.is_authenticated()
def get_services(
    request: Request,
    comm: CommonGetQuery = Depends(),
    page: Pagination = Depends(),
    item: ServiceQuery = Depends(),
):
    items = service.get_multi(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    return paginate(items=items, page=page.page, size=page.size)


@db.read_transaction
@router.get(
    "/{service_uid}",
    response_model=Union[
        # ChronosServiceReadExtended,
        KubernetesServiceReadExtended,
        # MarathonServiceReadExtended,
        # MesosServiceReadExtended,
        NovaServiceReadExtended,
        # OneDataServiceReadExtended,
        # RucioServiceReadExtended,
    ],
    summary="Read a specific service",
    description="Retrieve a specific service using its *uid*. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error.",
)
@flaat.is_authenticated()
def get_service(request: Request, item: Service = Depends(valid_service_id)):
    return item


@db.write_transaction
@router.patch(
    "/{service_uid}",
    response_model=Optional[
        Union[
            # ChronosServiceReadExtended,
            KubernetesServiceReadExtended,
            # MarathonServiceReadExtended,
            # MesosServiceReadExtended,
            NovaServiceReadExtended,
            # OneDataServiceReadExtended,
            # RucioServiceReadExtended,
        ]
    ],
    dependencies=[Depends(validate_new_service_values)],
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
@flaat.access_level("write")
def put_service(
    request: Request,
    update_data: Union[
        # ChronosServiceUpdate,
        KubernetesServiceUpdate,
        # MarathonServiceUpdate,
        # MesosServiceUpdate,
        NovaServiceUpdate,
        # OneDataServiceUpdate,
        # RucioServiceUpdate,
    ],
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
    summary="Delete a specific service",
    description="Delete a specific service using its *uid*. \
        Returns `no content`. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error. \
        On cascade, delete related quotas.",
)
@flaat.access_level("write")
def delete_services(request: Request, item: Service = Depends(valid_service_id)):
    if not service.remove(db_obj=item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )


@db.read_transaction
@router.get(
    "/{service_uid}/identity_providers",
    response_model=List[IdentityProviderRead],
    summary="Read service accessible identity providers",
    description="Retrieve all the identity providers the \
        service has access to. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error.",
)
@flaat.is_authenticated()
def get_service_identity_providers(
    request: Request,
    item: Service = Depends(valid_service_id),
):
    return item.provider.single().identity_providers.all()
