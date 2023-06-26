from fastapi import APIRouter, Depends, HTTPException, status
from neomodel import db
from typing import List, Optional, Union

from .crud import (
    create_user_group,
    edit_user_group,
    read_user_groups,
    remove_user_group,
)
from .dependencies import valid_user_group_id, is_unique_user_group
from .models import UserGroup as UserGroupModel
from .schemas import (
    UserGroup,
    UserGroupCreate,
    UserGroupExtended,
    UserGroupPatch,
    UserGroupQuery,
)
from ..pagination import Pagination, paginate
from ..query import CommonGetQuery
from ..service.schemas_extended import ServiceExtended


router = APIRouter(prefix="/user_groups", tags=["user_groups"])


@db.read_transaction
@router.get(
    "/",
    response_model=List[Union[UserGroupExtended, UserGroup]],
)
def get_user_groups(
    comm: CommonGetQuery = Depends(),
    page: Pagination = Depends(),
    item: UserGroupQuery = Depends(),
    extended: bool = False,
):
    items = read_user_groups(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    if extended:
        items = [
            UserGroupExtended(
                **item.__dict__,
                clusters=item.clusters(),
                flavors=item.flavors(),
                images=item.images()
            )
            for item in items
        ]
    return paginate(items=items, page=page.page, size=page.size)


@db.write_transaction
@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=UserGroup
)
def post_user_group(item: UserGroupCreate = Depends(is_unique_user_group)):
    return create_user_group(item)


@db.read_transaction
@router.get(
    "/{user_group_uid}",
    response_model=Union[UserGroupExtended, UserGroup],
)
def get_user_group(
    extended: bool = False, item: UserGroupModel = Depends(valid_user_group_id)
):
    if extended:
        return UserGroupExtended(
            **item.__dict__,
            clusters=item.clusters(),
            flavors=item.flavors(),
            images=item.images()
        )
    return item


@db.write_transaction
@router.patch("/{user_group_uid}", response_model=Optional[UserGroup])
def patch_user_group(
    update_data: UserGroupPatch,
    item: UserGroupModel = Depends(valid_user_group_id),
):
    return edit_user_group(old_item=item, new_item=update_data)


@db.write_transaction
@router.delete("/{user_group_uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_group(item: UserGroupModel = Depends(valid_user_group_id)):
    if not remove_user_group(item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )


@db.read_transaction
@router.get("/{user_group_uid}/services", response_model=List[ServiceExtended])
def read_user_group_services(
    item: UserGroupModel = Depends(valid_user_group_id),
):
    return item.services()
