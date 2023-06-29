from fastapi import APIRouter, Body, Depends, HTTPException, status
from neomodel import db
from typing import List, Optional

from ..dependencies import valid_user_group_id, is_unique_user_group
from ...crud import user_group
from ...models import UserGroup as UserGroupModel
from ...schemas import (
    UserGroup,
    UserGroupCreate,
    UserGroupQuery,
    UserGroupUpdate,
)
from ....cluster.schemas import Cluster
from ....flavor.schemas import Flavor
from ....image.schemas import Image
from ....pagination import Pagination, paginate
from ....query import CommonGetQuery
from ....service.schemas_extended import ServiceExtended


router = APIRouter(prefix="/user_groups", tags=["user_groups"])


@db.read_transaction
@router.get(
    "/",
    response_model=List[UserGroup],
)
def get_user_groups(
    comm: CommonGetQuery = Depends(),
    page: Pagination = Depends(),
    item: UserGroupQuery = Depends(),
):
    items = user_group.get_multi(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    return paginate(items=items, page=page.page, size=page.size)


@db.write_transaction
@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=UserGroup
)
def post_user_group(item: UserGroupCreate = Depends(is_unique_user_group)):
    return user_group.create(obj_in=item)


@db.read_transaction
@router.get("/{user_group_uid}", response_model=UserGroup)
def get_user_group(item: UserGroupModel = Depends(valid_user_group_id)):
    return item


@db.write_transaction
@router.put("/{user_group_uid}", response_model=Optional[UserGroup])
def put_user_group(
    item: UserGroupModel = Depends(valid_user_group_id),
    update_data: UserGroupUpdate = Body(),
):
    if item.name != update_data.name:
        is_unique_user_group(update_data)
    return user_group.update(db_obj=item, obj_in=update_data)


@db.write_transaction
@router.delete("/{user_group_uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_group(item: UserGroupModel = Depends(valid_user_group_id)):
    if not user_group.remove(db_obj=item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )


@db.read_transaction
@router.get("/{user_group_uid}/clusters", response_model=List[Cluster])
def read_user_group_clusters(
    item: UserGroupModel = Depends(valid_user_group_id),
):
    return item.clusters()


@db.read_transaction
@router.get("/{user_group_uid}/flavors", response_model=List[Flavor])
def read_user_group_flavors(
    item: UserGroupModel = Depends(valid_user_group_id),
):
    return item.flavors()


@db.read_transaction
@router.get("/{user_group_uid}/images", response_model=List[Image])
def read_user_group_images(
    item: UserGroupModel = Depends(valid_user_group_id),
):
    return item.images()


@db.read_transaction
@router.get("/{user_group_uid}/services", response_model=List[ServiceExtended])
def read_user_group_services(
    item: UserGroupModel = Depends(valid_user_group_id),
):
    return item.services()
