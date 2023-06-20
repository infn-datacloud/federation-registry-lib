from fastapi import APIRouter, Depends, HTTPException, status
from neomodel import db
from typing import List, Mapping, Optional, Union

from .utils import CommonGetQuery, Pagination, paginate
from .utils.validation import valid_user_group_id
from .. import crud, schemas

router = APIRouter(prefix="/user_groups", tags=["user_groups"])


@db.read_transaction
@router.get(
    "/",
    response_model=List[Union[schemas.UserGroupExtended, schemas.UserGroup]],
)
def read_user_groups(
    comm: CommonGetQuery = Depends(),
    page: Pagination = Depends(),
    item: schemas.UserGroupBase = Depends(),
    extended: bool = False,
):
    items = crud.get_user_groups(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    if extended:
        items = [
            schemas.UserGroupExtended(
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
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserGroup
)
def add_user_group(item: schemas.UserGroupCreate):
    db_item = crud.get_user_group(name=item.name)
    if db_item is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="UserGroup already registered",
        )
    return crud.create_user_group(item)


@db.read_transaction
@router.get(
    "/{uid}",
    response_model=Union[schemas.UserGroupExtended, schemas.UserGroup],
)
def read_user_group(
    extended: bool = False, item: Mapping = Depends(valid_user_group_id)
):
    if extended:
        return schemas.UserGroupExtended(
            **item.__dict__,
            clusters=item.clusters(),
            flavors=item.flavors(),
            images=item.images()
        )
    return item


@db.write_transaction
@router.patch("/{uid}", response_model=Optional[schemas.UserGroup])
def update_user_group(
    update_data: schemas.UserGroupUpdate,
    item: Mapping = Depends(valid_user_group_id),
):
    return crud.update_user_group(old_item=item, new_item=update_data)


@db.write_transaction
@router.delete("/{uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_group(item: Mapping = Depends(valid_user_group_id)):
    if not crud.remove_user_group(item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )


# @db.read_transaction
# @router.get("/{uid}/services", response_model=List[schemas.ServiceExtended])
# def read_user_group_services(uid: UUID):
#    db_item = crud.get_user_group(uid=str(uid).replace("-", ""))
#    if db_item is None:
#        raise HTTPException(
#            status_code=status.HTTP_404_NOT_FOUND, detail="UserGroup not found"
#        )
#    services = []
#    for service, prov_details, quotas in db_item.services():
#        services.append(
#            schemas.ServiceExtended(
#                **service.__dict__, details=prov_details, quotas=quotas
#            )
#        )
#    return services
#
