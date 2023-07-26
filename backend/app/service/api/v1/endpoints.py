from fastapi import APIRouter, Depends, HTTPException, Response, status
from neomodel import db
from typing import List, Optional, Union

from app.service.api.dependencies import (
    valid_service_id,
    validate_new_service_values,
)
from app.service.crud import service
from app.service.models import Service
from app.service.schemas import ServiceQuery, ServiceUpdate
from app.service.schemas_extended import (
    ChronosServiceReadExtended,
    KubernetesServiceReadExtended,
    MarathonServiceReadExtended,
    MesosServiceReadExtended,
    NovaServiceReadExtended,
    OneDataServiceReadExtended,
    RucioServiceReadExtended,
)
from app.identity_provider.schemas import IdentityProviderRead
from app.pagination import Pagination, paginate
from app.query import CommonGetQuery

router = APIRouter(prefix="/services", tags=["services"])


@db.read_transaction
@router.get(
    "/",
    response_model=List[
        Union[
            ChronosServiceReadExtended,
            KubernetesServiceReadExtended,
            MarathonServiceReadExtended,
            MesosServiceReadExtended,
            NovaServiceReadExtended,
            OneDataServiceReadExtended,
            RucioServiceReadExtended,
        ]
    ],
)
def get_services(
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
        ChronosServiceReadExtended,
        KubernetesServiceReadExtended,
        MarathonServiceReadExtended,
        MesosServiceReadExtended,
        NovaServiceReadExtended,
        OneDataServiceReadExtended,
        RucioServiceReadExtended,
    ],
)
def get_service(item: Service = Depends(valid_service_id)):
    return item


@db.write_transaction
@router.put(
    "/{service_uid}",
    response_model=Optional[
        Union[
            ChronosServiceReadExtended,
            KubernetesServiceReadExtended,
            MarathonServiceReadExtended,
            MesosServiceReadExtended,
            NovaServiceReadExtended,
            OneDataServiceReadExtended,
            RucioServiceReadExtended,
        ]
    ],
    dependencies=[Depends(validate_new_service_values)],
)
def put_service(
    update_data: ServiceUpdate,
    response: Response,
    item: Service = Depends(valid_service_id),
):
    db_item = service.update(db_obj=item, obj_in=update_data)
    if db_item is None:
        response.status_code = status.HTTP_304_NOT_MODIFIED
    return db_item


@db.write_transaction
@router.delete("/{service_uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_services(item: Service = Depends(valid_service_id)):
    if not service.remove(db_obj=item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )


@db.read_transaction
@router.get(
    "/{service_uid}/identity_providers",
    response_model=List[IdentityProviderRead],
)
def get_service_identity_providers(
    item: Service = Depends(valid_service_id),
):
    return item.provider.single().identity_providers.all()
