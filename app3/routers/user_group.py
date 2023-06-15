from fastapi import APIRouter, Depends, HTTPException, status
from neomodel import db
from typing import List, Optional
from uuid import UUID

from .utils import CommonGetQuery, Pagination, paginate
from .. import crud, schemas

router = APIRouter(prefix="/user_groups", tags=["user_groups"])


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
@router.get("/{uid}", response_model=schemas.UserGroup)
def read_user_group(uid: UUID):
    db_item = crud.get_user_group(uid=str(uid).replace("-", ""))
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="UserGroup not found"
        )
    return db_item


@db.write_transaction
@router.patch("/{uid}", response_model=Optional[schemas.UserGroup])
def update_user_group(uid: UUID, item: schemas.UserGroupUpdate):
    db_item = crud.get_user_group(uid=str(uid).replace("-", ""))
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="UserGroup not found"
        )
    return crud.update_user_group(old_item=db_item, new_item=item)


@db.write_transaction
@router.delete("/{uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_group(uid: UUID):
    db_item = crud.get_user_group(uid=str(uid).replace("-", ""))
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="UserGroup not found"
        )
    if not crud.remove_user_group(db_item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )


@db.read_transaction
@router.get("/", response_model=List[schemas.UserGroup])
def read_user_groups(
    comm: CommonGetQuery = Depends(),
    page: Pagination = Depends(),
    item: schemas.UserGroupBase = Depends(),
):
    items = crud.get_user_groups(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    return paginate(items=items, page=page.page, size=page.size)


# @db.write_transaction
# @router.post("/{uid}/projects", response_model=schemas.Project)
# def add_project_to_user_group(uid: str, item: schemas.ProjectCreate):
#    db_user_group = crud.get_user_group(uid=uid)
#    if db_user_group is None:
#        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="UserGroup not found")
#    db_project = crud.create_project(item=item)
#    if not crud.connect_project_to_user_group(
#        user_group=db_user_group, project=db_project
#    ):
#        raise HTTPException(
#            status_code=500, detail="Relationship creation failed"
#        )
#    return db_project


# @db.write_transaction
# @router.patch("/{uid}", response_model=schemas.UserGroup)
# def add_project_to_user_group(uid: str, item: schemas.UserGroupCreate):
#     db_user_group = crud.get_user_group(uid=uid)
#     if db_user_group is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="UserGroup not found")
#     update_data = item.dict(exclude_unset=True)
#     db_user_group = db_user_group.copy(update=update_data)
#     crud.replace_user_group()


#     db_project = crud.get_project(uid=project_id)
#     if db_project is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
#     if not crud.connect_project_to_user_group(
#         user_group=db_user_group, project=db_project
#     ):
#         raise HTTPException(
#             status_code=500, detail="Relationship creation failed"
#         )
#     db_user_group.refresh()
#     return db_user_group


# @db.write_transaction
# @router.put("/{uid}", response_model=schemas.UserGroup)
# def add_project_to_user_group(uid: UUID, project_id: str):
#    db_user_group = crud.get_user_group(uid=uid)
#    if db_user_group is None:
#        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="UserGroup not found")
#    db_project = crud.get_project(uid=project_id)
#    if db_project is None:
#        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
#    if not crud.connect_project_to_user_group(
#        user_group=db_user_group, project=db_project
#    ):
#        raise HTTPException(
#            status_code=500, detail="Relationship creation failed"
#        )
#    db_user_group.refresh()
#    return db_user_group
#
