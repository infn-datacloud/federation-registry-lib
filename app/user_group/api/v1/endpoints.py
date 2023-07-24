from fastapi import APIRouter, Depends, HTTPException, Response, status
from neomodel import db
from typing import List, Optional, Union

from app.auth.dependencies import get_current_active_user
from app.flavor.schemas import FlavorRead
from app.image.schemas import ImageRead
from app.pagination import Pagination, paginate
from app.provider.schemas import ProviderRead
from app.query import CommonGetQuery
from app.service.schemas_extended import (
    ChronosServiceReadExtended,
    KubernetesServiceReadExtended,
    MarathonServiceReadExtended,
    MesosServiceReadExtended,
    NovaServiceReadExtended,
    OneDataServiceReadExtended,
    RucioServiceReadExtended,
)
from app.user_group.api.dependencies import (
    valid_user_group_id,
    validate_new_user_group_values,
)
from app.user_group.crud import user_group
from app.user_group.models import UserGroup
from app.user_group.schemas import (
    UserGroupQuery,
    UserGroupUpdate,
)
from app.user_group.schemas_extended import UserGroupReadExtended, ServiceQuery

router = APIRouter(prefix="/user_groups", tags=["user_groups"])


@db.read_transaction
@router.get(
    "/",
    response_model=List[UserGroupReadExtended],
)
def get_user_groups(
    current_user: str = Depends(get_current_active_user),
    comm: CommonGetQuery = Depends(),
    page: Pagination = Depends(),
    item: UserGroupQuery = Depends(),
):
    print(current_user)
    items = user_group.get_multi(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    return paginate(items=items, page=page.page, size=page.size)


@db.read_transaction
@router.get("/{user_group_uid}", response_model=UserGroupReadExtended)
def get_user_group(item: UserGroup = Depends(valid_user_group_id)):
    return item


@db.write_transaction
@router.put(
    "/{user_group_uid}",
    response_model=Optional[UserGroupReadExtended],
    dependencies=[Depends(validate_new_user_group_values)],
)
def put_user_group(
    update_data: UserGroupUpdate,
    response: Response,
    item: UserGroup = Depends(valid_user_group_id),
):
    db_item = user_group.update(db_obj=item, obj_in=update_data)
    if db_item is None:
        response.status_code = status.HTTP_304_NOT_MODIFIED
    return db_item


@db.write_transaction
@router.delete("/{user_group_uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_group(item: UserGroup = Depends(valid_user_group_id)):
    if not user_group.remove(db_obj=item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )


@db.read_transaction
@router.get("/{user_group_uid}/flavors", response_model=List[FlavorRead])
def get_user_group_flavors(
    item: UserGroup = Depends(valid_user_group_id),
):
    return item.flavors()


@db.read_transaction
@router.get("/{user_group_uid}/images", response_model=List[ImageRead])
def get_user_group_images(
    item: UserGroup = Depends(valid_user_group_id),
):
    return item.images()


@db.read_transaction
@router.get("/{user_group_uid}/providers", response_model=List[ProviderRead])
def get_user_group_providers(
    item: UserGroup = Depends(valid_user_group_id),
):
    return item.providers()


@db.read_transaction
@router.get(
    "/{user_group_uid}/services",
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
def get_user_group_services(
    item: UserGroup = Depends(valid_user_group_id),
    service: ServiceQuery = Depends(),
):
    return item.services(**service.dict(exclude_none=True))
